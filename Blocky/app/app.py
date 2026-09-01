from flask import Flask
from extensions import db
import os

def create_app():
    app = Flask(__name__)

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    instance_dir = os.path.join(BASE_DIR, "instance")
    backups_dir = os.path.join(instance_dir, "backups")

    os.makedirs(instance_dir, exist_ok=True)
    os.makedirs(backups_dir, exist_ok=True)

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(instance_dir, 'Blocky.db')}"

    app.config["SQLALCHEMY_BINDS"] = {
        "backup1": f"sqlite:///{os.path.join(backups_dir, 'BlockBackup1.db')}",
        "backup2": f"sqlite:///{os.path.join(backups_dir, 'BlockBackup2.db')}",
        "backup3": f"sqlite:///{os.path.join(backups_dir, 'BlockBackup3.db')}",
    }

    db.init_app(app)

    from routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()  # creates ALL DBs: main + binds

    return app
