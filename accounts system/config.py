import os
from datetime import timedelta

class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Stuggy@4665@localhost/accounting_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

    # Application configuration
    SECRET_KEY = '7043548bd7594aeca104fc49d176a6d74fd5867b845f0cb5'  # Change this to a secure secret key
    DEBUG = True

    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)

    # API configuration
    API_TITLE = 'Security Company Accounting System'
    API_VERSION = 'v1'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False

# Get configuration based on environment
def get_config():
    env = os.getenv('FLASK_ENV', 'development')
    if env == 'production':
        return ProductionConfig
    return DevelopmentConfig