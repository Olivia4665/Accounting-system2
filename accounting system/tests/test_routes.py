import json

def test_create_account(test_client):
    data = {
        'code': '1001',
        'name': 'Cash',
        'type': 'Asset'
    }
    response = test_client.post('/api/accounts', json=data)
    assert response.status_code == 201
    assert json.loads(response.data)['message'] == 'Account created successfully'

def test_create_transaction(test_client):
    data = {
        'description': 'Test transaction',
        'entries': [
            {'account_id': 1, 'debit': 100.0, 'credit': 0.0},
            {'account_id': 2, 'debit': 0.0, 'credit': 100.0}
        ]
    }
    response = test_client.post('/api/transactions', json=data)
    assert response.status_code == 201
    assert json.loads(response.data)['message'] == 'Transaction recorded successfully'