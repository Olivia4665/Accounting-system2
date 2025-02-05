from app.models import User, Account, Transaction, TransactionEntry
from datetime import datetime

def test_user_model(test_app):
    user = User(username='testuser', password_hash='hash', role='admin')
    assert user.username == 'testuser'
    assert user.role == 'admin'

def test_account_model(test_app):
    account = Account(code='1001', name='Cash', type='Asset')
    assert account.code == '1001'
    assert account.type == 'Asset'

def test_transaction_model(test_app):
    transaction = Transaction(description='Test transaction')
    assert transaction.description == 'Test transaction'