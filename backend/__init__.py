from flask import Flask
from .resource import api


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("defaultSettings.py")
    api.init_app(app)
    return app


__all__ = [create_app]
