import os, threading, time
from flask import Flask
from flask_login import LoginManager
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
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
babel = Babel()

def create_app():
    app = Flask(__name__, instance_relative_config=True, static_folder=None)
    app.config.from_object(Config)

    os.makedirs("var/log", exist_ok=True)
    setup_logging(app)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    babel.init_app(app, default_locale=app.config["BABEL_DEFAULT_LOCALE"])

    register_i18n(app, babel)

    with app.app_context():
        db.create_all()
        # Ensure admin user exists
        if not User.query.filter_by(username=app.config["ADMIN_USERNAME"]).first():
            User.create_admin(app.config["ADMIN_USERNAME"], app.config["ADMIN_PASSWORD"])

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    register_update_routes(app)
    register_health(app)

    # Start control loop thread on first request
    cl = ControlLoop(app.config)
    @app.before_first_request
    def start_background():
        t = threading.Thread(target=cl.run, daemon=True)
        t.start()

    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
