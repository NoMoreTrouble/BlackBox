import os, threading
from flask import Flask
from flask_login import LoginManager
from .utils.logging_setup import setup_logging
from .utils.health import register_health
from .web.routes import bp as main_bp
from .web.auth import bp as auth_bp
from .web.api import bp as api_bp
from .web.i18n import register_i18n
from .models import db, User
from .control.controller import ControlLoop
from .utils.update import register_update_routes
from config import Config

login_manager = LoginManager()

def create_app(config_class: type[Config] = Config) -> Flask:
    app = Flask(__name__, static_folder="static", template_folder="web/templates")
    app.config.from_object(config_class)

    os.makedirs("var/log", exist_ok=True)
    setup_logging(app)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # i18n
    register_i18n(app)

    with app.app_context():
        db.create_all()
        admin_user = User.query.filter_by(username=app.config.get("ADMIN_USERNAME", "admin")).first()
        if not admin_user:
            User.create_admin(app.config.get("ADMIN_USERNAME", "admin"), app.config.get("ADMIN_PASSWORD", "changeme"))

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    register_update_routes(app)
    register_health(app)

    # Control loop
    cl = ControlLoop(app.config)
    app.extensions = getattr(app, "extensions", {})
    app.extensions["control_loop"] = cl

    @app.before_first_request
    def _start_background():
        t = threading.Thread(target=cl.run, daemon=True)
        t.start()

    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
