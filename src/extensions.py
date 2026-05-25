from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from apscheduler.schedulers.background import BackgroundScheduler


from src.config import Config

db = SQLAlchemy()
migrate = Migrate()

jwt = JWTManager()

api = Api(
    title='Flask-RestX API',
    version='1.0',
    description=(
        'Cookie-based JWT API with CSRF protection. '
        'Use /api/auth/login first to receive cookies, then send '
        'X-CSRF-ACCESS for protected endpoints and X-CSRF-REFRESH for /api/auth/refresh.'
    ),
    authorizations=Config.AUTHORIZATION,
    doc='/api'
)

scheduler = BackgroundScheduler(timezone="UTC")