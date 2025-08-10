from flask import request, session
from flask_babel import _, refresh

def register_i18n(app, babel):
    @babel.localeselector
    def get_locale():
        return session.get('lang') or request.accept_languages.best_match(app.config["BABEL_SUPPORTED_LOCALES"])

    @app.get("/lang/<locale>")
    def set_lang(locale):
        if locale in app.config["BABEL_SUPPORTED_LOCALES"]:
            session['lang'] = locale
            refresh()
        return ("", 204)
