from flask import Flask
from flask_restful import Api
from .config import Config
from .database import engine, Base
from .routes import initialize_routes
from dotenv import load_dotenv

"""
Load variables from .env YOU SHOULD CREATE .ENV IF YOU DON'T BIG PROBLEMS WILL HAPPEN 😀 just kidding dont forget to create .env
"""
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    Base.metadata.create_all(bind=engine)

    api = Api(app)

    initialize_routes(api)

    return app
