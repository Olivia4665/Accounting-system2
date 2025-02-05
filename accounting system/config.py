from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', '507e5aa738b70634')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://root:Stuggy%404665@localhost/accounting_db')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://root:Stuggy%404665@localhost/accounting_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

#print(f"Database URL from .env: {os.getenv('DATABASE_URL','mysql+pymysql://root:Stuggy%404665@localhost/accounting_db')}")  # Debug print
#print(f"SQLAlchemy URI: {Config.SQLALCHEMY_DATABASE_URI}")  # Debug print
