from extensions import db
from datetime import datetime


class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, unique=False)
    account_verified = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    last_login = db.Column(db.DateTime)

class UsersBackup1(db.Model):
    __bind_key__ = "backup1"
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, unique=False)
    account_verified = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    last_login = db.Column(db.DateTime)

class UsersBackup2(db.Model):
    __bind_key__ = "backup2"
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, unique=False)
    account_verified = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    last_login = db.Column(db.DateTime)

class UsersBackup3(db.Model):
    __bind_key__ = "backup3"
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, unique=False)
    account_verified = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    last_login = db.Column(db.DateTime)

# DATABASE MODELS
class DatabaseModels(db.Model):
    __tablename__ = "database_models"

    id = db.Column(db.Integer, primary_key=True)
    ModelName = db.Column(db.String(128), nullable=False)
    ModelDescription = db.Column(db.String(512), nullable=True)

# STORES THE DATABASE TABLES FOR EACH MODEL
class DatabaseTables(db.Model):
    __tablename__ = "database_tables"

    id = db.Column(db.Integer, primary_key=True)
    TableName = db.Column(db.String(128), nullable=False)
    TableDescription = db.Column(db.String(512), nullable=True)
    ModelID = db.Column(db.Integer, db.ForeignKey("database_models.id"), nullable=False)

# STORES THE DATABASE COLUMNS FOR EACH TABLE WHICH LINKS TO A SPECIFIC TABLE IN A MODEL
class DatabaseColumns(db.Model):
    __tablename__ = "database_columns"

    id = db.Column(db.Integer, primary_key=True)
    ColumnName = db.Column(db.String(128), nullable=False)
    ColumnDescription = db.Column(db.String(512), nullable=True)
    TableID = db.Column(db.Integer, db.ForeignKey("database_tables.id"), nullable=False)

#BLOCK SWARMS

#BUILDS

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