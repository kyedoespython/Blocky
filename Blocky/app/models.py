from extensions import db
from datetime import datetime


class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False, unique=False)
    account_verified = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime)

class UsersBackup1(db.Model):
    __bind_key__ = "backup1"
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False, unique=False)
    account_verified = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime)

class UsersBackup2(db.Model):
    __bind_key__ = "backup2"
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False, unique=False)
    account_verified = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime)

class UsersBackup3(db.Model):
    __bind_key__ = "backup3"
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False, unique=False)
    account_verified = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime)

class LoginAttempts(db.Model):
    __tablename__ = "login_attempts"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    login_date = db.Column(db.DateTime)

class LoginAttemptsBackup1(db.Model):
    __bind_key__ = "backup1"
    __tablename__ = "login_attempts"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    login_date = db.Column(db.DateTime)

class LoginAttemptsBackup2(db.Model):
    __bind_key__ = "backup2"
    __tablename__ = "login_attempts"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), nullable=False)

class LoginAttemptsBackup3(db.Model):
    __bind_key__ = "backup3"
    __tablename__ = "login_attempts"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    login_date = db.Column(db.DateTime)