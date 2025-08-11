from flask_babel import Babel
from flask import request

# Initialize Babel object
babel = Babel()

def get_locale():
    # This function determines which locale to use
    return 'en'  # Hardcoding 'en' just for now

def register_i18n(app):
    # Initialize Babel with the app and pass get_locale function
    babel.init_app(app, locale_selector=get_locale)

