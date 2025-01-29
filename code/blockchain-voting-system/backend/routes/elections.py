from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Election, User, Candidates
from extensions import db
from blockchain import Blockchain

election_routes = Blueprint('elections', __name__)
blockchain = Blockchain()


@election_routes.route('/get_elections', methods=['GET'])
@jwt_required()
def get_elections():
    elections = Election.query.all()
    data = []
    for election in elections:
        candidates = Candidates.query.filter_by(election_id=election.id).all()
        data.append({
            'id': election.id,
            'title': election.title,
            'start_credits': election.start_credits,
            'start_date': election.start_date,
            'end_date': election.end_date,
            'description': election.description,
            'status': election.status.value,
            'candidates': [{
                'id': candidat.id,
                'name': candidat.name,
                'description': candidat.description,
            } for candidat in candidates],
        })

    return jsonify(data), 200

@election_routes.route('/create_election', methods=['POST'])
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
   
    data = {'id': new_election.id,
            'title': new_election.title,
            'status': new_election.status,
            'created_at': new_election.created_at.isoformat()
    }
    return jsonify(data), 201


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

        # Fetch the voter from the database
        voter = db.session.get(User, current_user['id'])
        if not voter:
            return jsonify({'error': 'Voter not found'}), 404
        
        # Check if the election exists
        election = db.session.get(Election, data['election_id'])
        if not election:
            return jsonify({'error': 'Election not found'}), 404

        # Ensure election is open for voting
        if election.status.lower() != 'ongoing':
            return jsonify({'error': 'Voting is not allowed for this election'}), 400

        # Quadratic cost calculation
        votes = int(data['votes'])
        quadratic_cost = votes ** 2

        # Check if the voter has enough credits
        if quadratic_cost > voter.credits:
            return jsonify({'error': 'Insufficient credits to cast these votes'}), 400

        # Deduct credits and store the vote
        voter.credits -= quadratic_cost
        if voter.credits < 0:
            voter.credits = 0  # Reset to 0 if credits drop below 0
        db.session.commit()  # Save the changes to the database

        # Add the vote transaction to the blockchain
        # print("Adding transaction to blockchain...")
        blockchain.add_transaction(
            voter_id=current_user['id'],
            election_id=data['election_id'],
            votes=data['votes'],
            proposal=data['proposal']
        )
        # print("Transaction added:", blockchain.current_transactions)

        # Automatically create a block after every transaction for simplicity
        blockchain.create_block(previous_hash=blockchain.chain[-1]["hash"])
        print("Block created:", blockchain.chain[-1])

        return jsonify({'message': 'Vote submitted successfully'}), 201

    except Exception as e:
        print(f"Error during vote submission: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


@election_routes.route('/results/<int:election_id>', methods=['GET'])
def get_results(election_id):
    try:
        # print(f"Blockchain Transactions: {blockchain.chain}")  # Debugging
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
    election = db.session.get(Election, election_id)
    if not election:
        return jsonify({'error': 'Election not found'}), 404

    # Update the status
    election.status = new_status
    db.session.commit()

    return jsonify({'message': f'Election status updated to {new_status}'}), 200
