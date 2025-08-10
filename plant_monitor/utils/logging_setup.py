import logging, os
from logging.handlers import RotatingFileHandler

def _handler(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    h = RotatingFileHandler(path, maxBytes=2_000_000, backupCount=3)
    h.setFormatter(logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s'))
    return h

def setup_logging(app):
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    # Console for Docker
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s'))
    root.addHandler(ch)

    root.addHandler(_handler("var/log/app.log"))
    logging.getLogger("control").addHandler(_handler("var/log/control.log"))
    logging.getLogger("sensors").addHandler(_handler("var/log/sensors.log"))
    logging.getLogger("actuators").addHandler(_handler("var/log/actuators.log"))
    logging.getLogger("updates").addHandler(_handler("var/log/updates.log"))
