from flask import jsonify

def register_health(app):
    @app.get("/healthz")
    def health():
        return jsonify({"ok": True})
