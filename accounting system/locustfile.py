from locust import HttpUser, task, between

class AccountingSystemUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def create_account(self):
        self.client.post('/api/accounts', json={
            'code': '1001',
            'name': 'Cash',
            'type': 'Asset'
        })

    @task
    def create_transaction(self):
        self.client.post('/api/transactions', json={
            'description': 'Test transaction',
            'entries': [
                {'account_id': 1, 'debit': 100.0, 'credit': 0.0},
                {'account_id': 2, 'debit': 0.0, 'credit': 100.0}
            ]
        })