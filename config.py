import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration shared by all environments."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-in-production")
    DEBUG = False
    TESTING = False

    # Site metadata
    SITE_NAME = "DXC.GE"
    SITE_FULL_NAME = "Digital X Control"
    SITE_TAGLINE = "Your Trusted Security & Technology Partner in Georgia"
    SITE_EMAIL = "info@dxc.ge"
    SITE_PHONE = "+995 XXX XXX XXX"
    SITE_ADDRESS = "Tbilisi, Georgia"


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, 'dxc_dev.db')}"
    )


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY")  # Must be set in environment
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


config_map = {
    "development": DevelopmentConfig,
    "production":  ProductionConfig,
    "testing":     TestingConfig,
}
