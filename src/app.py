from flask import Flask
from routes import auth_bp, document_bp, chat_bp
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(auth_bp)
    app.register_blueprint(document_bp)
    app.register_blueprint(chat_bp)

    return app


