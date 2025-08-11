import subprocess, threading, logging, requests
from flask import Blueprint, request, jsonify, current_app
from ..models import db, UpdateLog

log = logging.getLogger("updates")

def notify(msg):
    token = current_app.config.get("TELEGRAM_BOT_TOKEN")
    chat = current_app.config.get("TELEGRAM_CHAT_ID")
    if token and chat:
        try:
            requests.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={"chat_id": chat, "text": msg}, timeout=5
            )
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
        last = UpdateLog.query.order_by(UpdateLog.id.desc()).limit(20).all()
        # Render via template name; avoids importing render_template here
        return app.jinja_env.get_or_select_template("update.html").render(logs=last)

    @bp.route("/webhook/update", methods=["POST"])
    def webhook_update():
        token = request.headers.get("X-Update-Token") or request.args.get("token")
        if token != app.config.get("UPDATE_WEBHOOK_TOKEN"):
            return jsonify({"error": "unauthorized"}), 401

        def worker():
            db.session.add(UpdateLog(status="started", message="Update started"))
            db.session.commit()
            notify("Update started")

            rc = 0
            msgs = []
            try:
                # Example flow: git pull + pip install
                for line in _run_cmd(["git", "pull", "--rebase"]):
                    msgs.append(line)
                for line in _run_cmd(["pip", "install", "-r", "requirements.txt"]):
                    msgs.append(line)
            except Exception as e:
                rc = 1
                msgs.append(str(e))

            status = "success" if rc == 0 else "failure"
            notify(f"Update {status}.")
            db.session.add(UpdateLog(status=status, message="".join(msgs)))
            db.session.commit()

        threading.Thread(target=worker, daemon=True).start()
        return jsonify({"ok": True})

    app.register_blueprint(bp)
