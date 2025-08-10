import os, pytest
os.environ.setdefault("MODE", "SIMULATION")
os.environ.setdefault("FLASK_SECRET_KEY", "test")
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

from plant_monitor import create_app
from plant_monitor.models import db

@pytest.fixture()
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app

@pytest.fixture()
def client(app):
    return app.test_client()
