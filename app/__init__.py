# app/__init__.py

from flask import Flask
from flask_restful import Api
from .config import Config
from .database import engine, Base
from .routes import initialize_routes
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the database
    Base.metadata.create_all(bind=engine)

    # Initialize Flask-RESTful API
    api = Api(app)

    # Initialize API routes
    initialize_routes(api)

    return app
