from extensions import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False, unique=False)

    account_verified = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime)


class LoginAttempts(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), nullable=False)

    login_date = db.Column(db.DateTime)