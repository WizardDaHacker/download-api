from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

class Download(db.Model):

    hash = db.Column(db.String(32), primary_key=True)
    file_name = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=True)
    data = db.Column(db.PickleType(), nullable=False)

    session_id = db.Column(db.Integer, db.ForeignKey("session.id"), nullable=False, unique=False)
    session = db.relationship("Session", backref=db.backref("downloads", lazy=True))

class Session(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    directory = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)