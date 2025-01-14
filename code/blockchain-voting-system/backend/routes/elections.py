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
    } for election in elections])

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

@election_routes.route('/vote', methods=['POST'])
@jwt_required()
def submit_vote():
    data = request.get_json()
    current_user = get_jwt_identity()

    election = Election.query.get(data.get('election_id'))
    if not election:
        return jsonify({'error': 'Election not found'}), 404

    new_vote = Vote(
        election_id=data.get('election_id'),
        user_id=current_user['id'],
        proposal=data.get('proposal'),
        votes=data.get('votes')
    )
    db.session.add(new_vote)
    db.session.commit()
    return jsonify({'message': 'Vote submitted successfully'}), 201

