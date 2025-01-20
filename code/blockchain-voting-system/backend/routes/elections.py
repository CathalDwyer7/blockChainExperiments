from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Election, Vote
from extensions import db

election_routes = Blueprint('elections', __name__)

@election_routes.route('/', methods=['GET'])
def get_elections():
    elections = Election.query.all()
    return jsonify([{
        'id': election.id,
        'title': election.title,
        'status': election.status,
        'created_at': election.created_at.isoformat()
    } for election in elections]), 200

@election_routes.route('/', methods=['POST'])
@jwt_required()
def create_election():
    data = request.get_json()
    current_user = get_jwt_identity()

    if current_user['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    new_election = Election(title=data.get('title'), status='Upcoming')
    db.session.add(new_election)
    db.session.commit()
    return jsonify({'message': 'Election created successfully'}), 201

from blockchain import blockchain

@election_routes.route('/vote', methods=['POST'])
@jwt_required()
def submit_vote():
    current_user = get_jwt_identity()
    data = request.get_json()

    # Validate input
    if not data or 'election_id' not in data or 'votes' not in data:
        return jsonify({'error': 'Invalid request, election_id and votes are required'}), 400

    # Check if the election exists
    election = Election.query.get(data['election_id'])
    if not election:
        return jsonify({'error': 'Election not found'}), 404

    # Ensure election is open for voting
    if election.status.lower() != 'ongoing':
        return jsonify({'error': 'Voting is not allowed for this election'}), 400

    # Add the vote transaction to the blockchain
    voter_id = current_user['id']
    blockchain.add_transaction(voter_id, data['election_id'], data['votes'])
    return jsonify({'message': 'Vote submitted successfully'}), 201
