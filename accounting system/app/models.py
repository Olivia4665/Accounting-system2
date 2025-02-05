from app import db
from datetime import datetime
from sqlalchemy import CheckConstraint

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role
        }

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # Asset, Liability, Equity, Revenue, Expense
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    entries = db.relationship('TransactionEntry', backref='account', lazy=True)

    # Validation for account type
    __table_args__ = (
        CheckConstraint(
            type.in_(['Asset', 'Liability', 'Equity', 'Revenue', 'Expense']),
            name='check_account_type'
        ),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'type': self.type,
            'created_at': self.created_at.isoformat()
        }

    def calculate_balance(self):
        """Calculate the account balance based on transaction entries."""
        debits = sum(entry.debit for entry in self.entries)
        credits = sum(entry.credit for entry in self.entries)
        if self.type in ['Asset', 'Expense']:
            return debits - credits
        else:
            return credits - debits

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.String(200))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Relationships
    entries = db.relationship('TransactionEntry', backref='transaction', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'description': self.description,
            'created_by': self.created_by,
            'entries': [entry.to_dict() for entry in self.entries]
        }

class TransactionEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'))
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    debit = db.Column(db.Float, default=0.0)
    credit = db.Column(db.Float, default=0.0)

    def to_dict(self):
        return {
            'id': self.id,
            'transaction_id': self.transaction_id,
            'account_id': self.account_id,
            'debit': self.debit,
            'credit': self.credit
        }