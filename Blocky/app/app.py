from flask import Flask
from flask_migrate import Migrate
from extensions import db
from sqlalchemy import inspect, text
from werkzeug.security import generate_password_hash
import click
import os

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    instance_dir = os.path.join(BASE_DIR, "instance")
    backups_dir = os.path.join(instance_dir, "backups")

    os.makedirs(instance_dir, exist_ok=True)
    os.makedirs(backups_dir, exist_ok=True)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")

    def backup_uri(name):
        value = os.getenv(name)
        if value and "://" in value:
            return value
        return f"sqlite:///{os.path.join(backups_dir, value or name + '.db')}"

    app.config["SQLALCHEMY_BINDS"] = {
        "backup1": backup_uri("DATABASE_URI_BACKUP1"),
        "backup2": backup_uri("DATABASE_URI_BACKUP2"),
        "backup3": backup_uri("DATABASE_URI_BACKUP3"),
    }

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate = Migrate(app, db)
    import models

    with app.app_context():
        db.create_all()
        for engine in db.engines.values():
            if "is_admin" not in {column["name"] for column in inspect(engine).get_columns("users")}:
                with engine.begin() as connection:
                    connection.execute(text("ALTER TABLE users ADD COLUMN is_admin BOOLEAN NOT NULL DEFAULT FALSE"))
        _ensure_admin_account()

    from routes import main
    app.register_blueprint(main)

    @app.cli.command("grant-admin")
    @click.argument("username")
    def grant_admin(username):
        from models import Users, UsersBackup1, UsersBackup2, UsersBackup3

        user = Users.query.filter_by(username=username).first()
        if not user:
            click.echo(f"User not found: {username}")
            return
        user.is_admin = True
        for backup_model in (UsersBackup1, UsersBackup2, UsersBackup3):
            backup_user = backup_model.query.filter_by(username=username).first()
            if backup_user:
                backup_user.is_admin = True
        db.session.commit()
        click.echo(f"Administrator privilege granted to {username}")

    return app


def _ensure_admin_account():
    username = os.getenv("ADMIN_USERNAME")
    password = os.getenv("ADMIN_PASSWORD")
    email = os.getenv("ADMIN_EMAIL")
    if not username or not password or not email:
        return

    from models import Users, UsersBackup1, UsersBackup2, UsersBackup3

    user = Users.query.filter_by(username=username).first()
    if not user:
        user = Users(username=username, email=email, password=generate_password_hash(password), is_admin=True)
        db.session.add(user)
        db.session.flush()
    else:
        user.email = email
        user.password = generate_password_hash(password)
        user.is_admin = True

    for backup_model in (UsersBackup1, UsersBackup2, UsersBackup3):
        backup_user = backup_model.query.filter_by(username=username).first()
        if not backup_user:
            backup_user = backup_model(id=user.id, username=username, email=email,
                                       password=user.password, is_admin=True)
            db.session.add(backup_user)
        else:
            backup_user.email = email
            backup_user.password = user.password
            backup_user.is_admin = True
    db.session.commit()
