from flask import Flask
from flask_cors import CORS

# Import models before migration commands inspect SQLAlchemy metadata.
from . import models
from .cli import register_commands
from .config import config_by_name
from .extensions import db, migrate
from .routes import api_bp, auth_bp


def create_app(config_name=None):
    app = Flask(__name__)
    selected_config = config_name or "development"
    app.config.from_object(config_by_name.get(selected_config, config_by_name["development"]))

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(
        app,
        resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}},
        supports_credentials=True,
    )

    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    register_commands(app)

    return app
