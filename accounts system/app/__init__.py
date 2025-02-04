
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import get_config
import pymysql

# Initialize extensions
db = SQLAlchemy()

def create_app():
    # Initialize Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(get_config())
    
    # Initialize database
    pymysql.install_as_MySQLdb()
    db.init_app(app)
    
    # Register blueprints
    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        initialize_default_accounts()
    
    return app

def initialize_default_accounts():
    from app.models import Account
    
    # Check if we need to create initial accounts
    if Account.query.count() == 0:
        # Create basic accounts for security company
        default_accounts = [
            Account(code='1000', name='Cash', type='asset', category='current'),
            Account(code='1200', name='Security Equipment', type='asset', category='fixed'),
            Account(code='2000', name='Accounts Payable', type='liability', category='current'),
            Account(code='3000', name='Owner\'s Equity', type='equity', category='equity'),
            Account(code='4000', name='Security Services Revenue', type='revenue', category='operating'),
            Account(code='5000', name='Security Personnel Expenses', type='expense', category='operating')
        ]
        db.session.bulk_save_objects(default_accounts)
        db.session.commit()