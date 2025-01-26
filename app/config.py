import os

from dotenv import load_dotenv

"""
Load variables from .env YOU SHOULD CREATE .ENV IF YOU DON'T BIG PROBLEMS WILL HAPPEN 😀 just kidding dont forget to create .env
"""
load_dotenv()


class Config:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
