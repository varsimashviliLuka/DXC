from dotenv import load_dotenv
import os
from datetime import timedelta
from pathlib import Path

# Load environment variables from .env
load_dotenv(dotenv_path="./.env")

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent

class Config(object):
    SECRET_KEY = os.getenv("MY_SECRET_KEY", "default_secret_key")
    BASE_DIR = BASE_DIR
    TEMPLATES_FOLDERS = "src/templates"

    DEBUG = False

    RESTX_MASK_SWAGGER = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'app.sqlite3'}")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_jwt_secret_key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=12)
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_TOKEN_LOCATION = ["headers","cookies"]
    JWT_COOKIE_SECURE = False # True in production (HTTPS)
    JWT_COOKIE_SAMESITE = "Strict"
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_ACCESS_COOKIE_PATH = "/"
    JWT_REFRESH_COOKIE_PATH = "/api/auth/refresh"
    JWT_REFRESH_COOKIE_NAME = "refresh_token"

    AUTHORIZATION = {
        "JsonWebToken": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization"
        }
    }

    MAIL_SERVER = os.getenv("MAIL_SERVER", "MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT", "MAIL_PORT")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "MAIL_PASSWORD")

    TOKEN_ENCRYPTION_KEY = os.getenv("TOKEN_ENCRYPTION_KEY", "default_token_encryption_key")

    CLIENT_ID = os.getenv("CLIENT_ID", "default_client_id")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET", "default_client_secret")

    ACCOUNT_NUMBER = os.getenv("ACCOUNT_NUMBER", "default_account_number")
    CURRENCY = os.getenv("CURRENCY", "default_currency")

class TestConfig(Config):
    DEBUG = True
    # Separate SQLite DB for tests
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=1)
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'test.sqlite3'}"