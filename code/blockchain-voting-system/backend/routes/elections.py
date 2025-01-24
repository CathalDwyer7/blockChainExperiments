from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Election
from extensions import db
from blockchain import Blockchain

election_routes = Blueprint('elections', __name__)
blockchain = Blockchain()


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

    if 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400

    new_election = Election(title=data.get('title'), status='Upcoming')
    db.session.add(new_election)
    db.session.commit()
    return jsonify({'message': 'Election created successfully'}), 201


@election_routes.route('/vote', methods=['POST'])
@jwt_required()
def submit_vote():
    try:

        current_user = get_jwt_identity()
        data = request.get_json()
        
        print(f"Current User: {current_user}")
        print(f"Request Data: {data}")

        # Validate input
        if 'election_id' not in data or 'votes' not in data or 'proposal' not in data:
            return jsonify({'error': 'Invalid request. election_id, votes, and proposal are required'}), 400

        # Check if the election exists
        election = Election.query.get(data['election_id'])
        if not election:
            return jsonify({'error': 'Election not found'}), 404

        # Ensure election is open for voting
        if election.status.lower() != 'ongoing':
            return jsonify({'error': 'Voting is not allowed for this election'}), 400
  
        # Add the vote transaction to the blockchain
        print("Adding transaction to blockchain...")
        blockchain.add_transaction(
           voter_id=current_user['id'],
            election_id=data['election_id'],
            votes=data['votes'],
            proposal=data['proposal']
        )
        print("Transaction added:", blockchain.current_transactions)

        # Automatically create a block after every transaction for simplicity
        blockchain.create_block(previous_hash=blockchain.chain[-1]["hash"])
        print("Block created:", blockchain.chain[-1])
        
        return jsonify({'message': 'Vote submitted successfully'}), 201


    except Exception as e:
        print(f"Error during vote submission: {e}")
        return jsonify({'error':'Internal Server Error'}), 500


@election_routes.route('/results/<int:election_id>', methods=['GET'])
def get_results(election_id):
    try:
        print(f"Blockchain Transactions: {blockchain.chain}")  # Debugging
        results = blockchain.tally_votes(election_id)
        return jsonify({
            'election_id': election_id,
            'results': results
        }), 200
    except Exception as e:
        print(f"Error during result tallying: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


@election_routes.route('/<int:election_id>/status', methods=['PATCH'])
@jwt_required()
def update_election_status(election_id):
    """Update the status of an election (admin only)."""
    current_user = get_jwt_identity()

    # Only admins can update the election status
    if current_user['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    new_status = data.get('status')

    # Validate the new status
    if not new_status or new_status not in ['Upcoming', 'Ongoing', 'Completed']:
        return jsonify({'error': 'Invalid status'}), 400

    # Find the election
    election = Election.query.get(election_id)
    if not election:
        return jsonify({'error': 'Election not found'}), 404

    # Update the status
    election.status = new_status
    db.session.commit()

    return jsonify({'message': f'Election status updated to {new_status}'}), 200
