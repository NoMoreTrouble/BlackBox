import os, subprocess, threading, logging, time, json
from flask import Blueprint, request, jsonify, current_app
from ..models import db, UpdateLog
import requests

log = logging.getLogger("updates")

def notify(msg):
    token = current_app.config.get("TELEGRAM_BOT_TOKEN")
    chat = current_app.config.get("TELEGRAM_CHAT_ID")
    if token and chat:
        try:
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                          json={"chat_id": chat, "text": msg}, timeout=5)
        except Exception as e:
            log.error("Telegram notify failed: %s", e)

def _run_cmd(cmd, cwd=None):
    p = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in iter(p.stdout.readline, ''):
        yield line
    p.wait()
    yield f"__RC={p.returncode}\n"

def register_update_routes(app):
    bp = Blueprint("updates", __name__)

    @bp.route("/updates", methods=["GET"])
    def updates_page():
        # Simple streaming is out of scope here; show last logs
        last = UpdateLog.query.order_by(UpdateLog.id.desc()).limit(20).all()
        return app.jinja_env.get_or_select_template("update.html").render(logs=last)

    @bp.route("/webhook/update", methods=["POST"])
    def webhook_update():
        token = request.headers.get("X-Update-Token") or request.args.get("token")
        if token != app.config["UPDATE_WEBHOOK_TOKEN"]:
            return jsonify({"error": "unauthorized"}), 401

        def worker():
            db.session.add(UpdateLog(status="started", message="Update started"))
            db.session.commit()
            notify("Update started")

            rc = 0
            msgs = []
            try:
                for line in _run_cmd(["git", "rev-parse", "HEAD"]):
                    head = line.strip()
                    if head.startswith("__RC"): break
                old_head = head

                for line in _run_cmd(["git", "pull", "--rebase"]):
                    msgs.append(line)
                # Reinstall deps (best-effort)
                for line in _run_cmd(["pip", "install", "-r", "requirements.txt"]):
                    msgs.append(line)

                # Docker rebuild if enabled
                if app.config.get("ENABLE_DOCKER_REBUILD"):
                    for line in _run_cmd(["docker", "compose", "-f", app.config["DOCKER_COMPOSE_FILE_PATH"], "up", "-d", "--build"]):
                        msgs.append(line)

            except Exception as e:
                rc = 1
                msgs.append(str(e))

            if rc != 0 or any("__RC=" in m and m.strip() != "__RC=0" for m in msgs):
                # Rollback
                _ = list(_run_cmd(["git", "reset", "--hard", old_head]))
                status = "failure"
                notify("Update failed — rolled back.")
            else:
                status = "success"
                notify("Update completed successfully.")

            db.session.add(UpdateLog(status=status, message="".join(msgs)))
            db.session.commit()

        threading.Thread(target=worker, daemon=True).start()
        return jsonify({"ok": True})

    app.register_blueprint(bp)
