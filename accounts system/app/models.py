from datetime import datetime
from app import db
from decimal import Decimal

class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Enum('asset', 'liability', 'equity', 'revenue', 'expense'), nullable=False)
    category = db.Column(db.String(50))
    balance = db.Column(db.Decimal(precision=15, scale=2), default=0)
    parent_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    reference = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    entries = db.relationship('TransactionEntry', backref='transaction', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TransactionEntry(db.Model):
    __tablename__ = 'transaction_entries'
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    debit = db.Column(db.Decimal(precision=15, scale=2), default=0)
    credit = db.Column(db.Decimal(precision=15, scale=2), default=0)

class SecurityAsset(db.Model):
    __tablename__ = 'security_assets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    asset_type = db.Column(db.Enum('vehicle', 'equipment', 'uniform', 'communication_device', 
                                  'surveillance_system', 'weapon', 'access_control'), nullable=False)
    serial_number = db.Column(db.String(50), unique=True)
    purchase_date = db.Column(db.DateTime, nullable=False)
    purchase_value = db.Column(db.Decimal(precision=15, scale=2), nullable=False)
    current_value = db.Column(db.Decimal(precision=15, scale=2), nullable=False)
    depreciation_method = db.Column(db.String(50))
    depreciation_rate = db.Column(db.Decimal(precision=5, scale=2))
    maintenance_schedule = db.Column(db.String(100))
    last_maintenance_date = db.Column(db.DateTime)
    next_maintenance_date = db.Column(db.DateTime)
    assigned_to = db.Column(db.String(100))
    location = db.Column(db.String(100))
    status = db.Column(db.Enum('active', 'maintenance', 'retired', 'lost'), default='active')
    license_expiry = db.Column(db.DateTime)

class SecurityInventory(db.Model):
    __tablename__ = 'security_inventory'
    id = db.Column(db.Integer, primary_key=True)
    item_code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.Enum('uniform', 'equipment', 'supplies', 'ammunition', 
                                'communication', 'safety_gear'), nullable=False)
    description = db.Column(db.String(200))
    quantity = db.Column(db.Integer, default=0)
    unit_cost = db.Column(db.Decimal(precision=15, scale=2))
    reorder_level = db.Column(db.Integer)
    supplier = db.Column(db.String(100))
    location = db.Column(db.String(100))
    expiry_date = db.Column(db.DateTime)
    restricted_access = db.Column(db.Boolean, default=False)

class SecurityContract(db.Model):
    __tablename__ = 'security_contracts'
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    contract_number = db.Column(db.String(50), unique=True, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    contract_value = db.Column(db.Decimal(precision=15, scale=2), nullable=False)
    billing_cycle = db.Column(db.String(20))
    payment_terms = db.Column(db.String(200))
    service_type = db.Column(db.String(100))
    status = db.Column(db.Enum('active', 'pending', 'completed', 'terminated'), default='active')