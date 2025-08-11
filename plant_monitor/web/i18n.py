try:
    from flask_babel import Babel
except Exception:
    Babel = None
from flask import request, session

babel = Babel() if Babel else None

def register_i18n(app):
    if babel is None:
        # Babel not installed; provide a no-op locale setter
        @app.get("/lang/<locale>")
        def set_lang(locale):
            session["lang"] = locale
            return ("", 204)
        return

    app.config.setdefault("BABEL_SUPPORTED_LOCALES", ["en", "it"])
    def _selector():
        return session.get("lang") or request.accept_languages.best_match(app.config["BABEL_SUPPORTED_LOCALES"])
    babel.init_app(app, locale_selector=_selector)

    @app.get("/lang/<locale>")
    def set_lang(locale):
        if locale in app.config["BABEL_SUPPORTED_LOCALES"]:
            session["lang"] = locale
        return ("", 204)
