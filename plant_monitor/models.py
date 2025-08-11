from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    @classmethod
    def create_admin(cls, username, password):
        u = cls(username=username, password_hash=generate_password_hash(password))
        db.session.add(u)
        db.session.commit()
        return u

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Reading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ts = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    soil1 = db.Column(db.Float)
    soil2 = db.Column(db.Float)
    soil3 = db.Column(db.Float)
    soil_avg = db.Column(db.Float)
    soil_avg_ewma = db.Column(db.Float)
    water_level_pct = db.Column(db.Float)

class ActuationLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ts = db.Column(db.DateTime, default=datetime.utcnow)
    device = db.Column(db.String(32)) # "light" or "irrigation"
    action = db.Column(db.String(32)) # "on"/"off"/"pulse"
    duration = db.Column(db.Integer, default=0)

class UpdateLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ts = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(32)) # started/success/failure
    message = db.Column(db.Text)
