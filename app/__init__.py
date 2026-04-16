from flask import Flask
from app.db import init_db


def create_app():
    app = Flask(__name__)
    app.config["DATABASE"] = "demo.db"

    with app.app_context():
        init_db(app)

    from app.dashboard import bp as dashboard_bp
    app.register_blueprint(dashboard_bp)

    return app
