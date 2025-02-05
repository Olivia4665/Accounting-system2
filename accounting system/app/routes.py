from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Account, Transaction, TransactionEntry
from app import db
from sqlalchemy.exc import SQLAlchemyError

# Create a Blueprint for your API
api = Blueprint('api', __name__)

# Add a route for the root URL
@api.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the accounting system API!"})

@api.route('/accounts', methods=['POST'])
@jwt_required()
def create_account():
    data = request.get_json()
    
    # Validate required fields
    if not all(key in data for key in ['code', 'name', 'type']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        account = Account(
            code=data['code'],
            name=data['name'],
            type=data['type']
        )
        db.session.add(account)
        db.session.commit()
        return jsonify({'message': 'Account created successfully', 'data': account.to_dict()}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create account', 'details': str(e)}), 500

@api.route('/transactions', methods=['POST'])
@jwt_required()
def create_transaction():
    data = request.get_json()
    
    # Validate required fields
    if not all(key in data for key in ['description', 'entries']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Validate debits equal credits
    total_debits = sum(entry.get('debit', 0) for entry in data['entries'])
    total_credits = sum(entry.get('credit', 0) for entry in data['entries'])
    
    if abs(total_debits - total_credits) > 0.001:
        return jsonify({'error': 'Debits must equal credits'}), 400
    
    try:
        transaction = Transaction(
            description=data['description'],
            created_by=get_jwt_identity()
        )
        
        for entry in data['entries']:
            if not all(key in entry for key in ['account_id', 'debit', 'credit']):
                return jsonify({'error': 'Missing required fields in transaction entry'}), 400
            
            transaction_entry = TransactionEntry(
                account_id=entry['account_id'],
                debit=entry['debit'],
                credit=entry['credit']
            )
            transaction.entries.append(transaction_entry)
        
        db.session.add(transaction)
        db.session.commit()
        return jsonify({'message': 'Transaction recorded successfully', 'data': transaction.to_dict()}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to record transaction', 'details': str(e)}), 500