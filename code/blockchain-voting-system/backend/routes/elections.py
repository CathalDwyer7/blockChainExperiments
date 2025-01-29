from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Election, User, Candidates
from extensions import db
from blockchain import Blockchain
from .auth import admin_required

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


@election_routes.route('/get_election/<int:id>', methods=['GET'])
@jwt_required()
def get_election_by_id(id):
    election = Election.query.get(id)

    if election is None:
        return jsonify({'error': 'Election not found'}), 404 

    candidates = Candidates.query.filter_by(election_id=election.id).all()

    data = {
        'id': election.id,
        'title': election.title,
        'start_credits': election.start_credits,
        'start_date': election.start_date,
        'end_date': election.end_date,
        'description': election.description,
        'status': election.status.value,
        'candidates': [{
            'id': candidate.id,
            'name': candidate.name,
            'description': candidate.description,
        } for candidate in candidates]
    }
    return jsonify(data), 200


@election_routes.route('/create_election', methods=['POST'])
@admin_required
def create_election():
    data = request.get_json()

    required_fields = ['title', 'start_credits', 'start_date', 'end_date', 'description']
    missing_fields = [filed for filed in required_fields if filed not in data]

    if missing_fields:
        return jsonify({'error': f'{", ".join(missing_fields)} are required'}), 400

    new_election = Election(
        title=data.get('title'),
        start_credits=int(data.get('start_credits')),
        start_date=int(data.get('start_date')),
        end_date=int(data.get('end_date')),
        description=data.get('description')
    )
    db.session.add(new_election)
    db.session.commit()

    if 'candidates' in data:
        for c in data['candidates']:
            new_candidate = Candidates(
                election_id=new_election.id,
                name=c['name'],
                description=c.get('description','')
            )
            db.session.add(new_candidate)
        db.session.commit()


    candidates = Candidates.query.filter_by(election_id=new_election.id).all()

    output_data = {
        'id':new_election.id,
        'title':new_election.title,
        'start_credits':new_election.start_credits,
        'start_date':new_election.start_date,
        'end_date':new_election.end_date,
        'description':new_election.description,
        'candidates': [{'id': c.id, 'name': c.name, 'description': c.description} for c in candidates]
    }
    return jsonify(output_data), 201


#@election_routes.route('/vote', methods=['POST'])
#@jwt_required()
#def submit_vote():
#    try:
#
#        current_user = get_jwt_identity()
#        data = request.get_json()
#
#        print(f"Current User: {current_user}")
#        print(f"Request Data: {data}")
#
#        # Validate input
#        if 'election_id' not in data or 'votes' not in data or 'proposal' not in data:
#            return jsonify({'error': 'Invalid request. election_id, votes, and proposal are required'}), 400
#
#        # Fetch the voter from the database
#        voter = db.session.get(User, current_user['id'])
#        if not voter:
#            return jsonify({'error': 'Voter not found'}), 404
#        
#        # Check if the election exists
#        election = db.session.get(Election, data['election_id'])
#        if not election:
#            return jsonify({'error': 'Election not found'}), 404
#
#        # Ensure election is open for voting
#        if election.status.lower() != 'ongoing':
#            return jsonify({'error': 'Voting is not allowed for this election'}), 400
#
#        # Quadratic cost calculation
#        votes = int(data['votes'])
#        quadratic_cost = votes ** 2
#
#        # Check if the voter has enough credits
#        if quadratic_cost > voter.credits:
#            return jsonify({'error': 'Insufficient credits to cast these votes'}), 400
#
#        # Deduct credits and store the vote
#        voter.credits -= quadratic_cost
#        if voter.credits < 0:
#            voter.credits = 0  # Reset to 0 if credits drop below 0
#        db.session.commit()  # Save the changes to the database
#
#        # Add the vote transaction to the blockchain
#        # print("Adding transaction to blockchain...")
#        blockchain.add_transaction(
#            voter_id=current_user['id'],
#            election_id=data['election_id'],
#            votes=data['votes'],
#            proposal=data['proposal']
#        )
#        # print("Transaction added:", blockchain.current_transactions)
#
#        # Automatically create a block after every transaction for simplicity
#        blockchain.create_block(previous_hash=blockchain.chain[-1]["hash"])
#        print("Block created:", blockchain.chain[-1])
#
#        return jsonify({'message': 'Vote submitted successfully'}), 201
#
#    except Exception as e:
#        print(f"Error during vote submission: {e}")
#        return jsonify({'error': 'Internal Server Error'}), 500
#
#
#@election_routes.route('/results/<int:election_id>', methods=['GET'])
#def get_results(election_id):
#    try:
#        # print(f"Blockchain Transactions: {blockchain.chain}")  # Debugging
#        results = blockchain.tally_votes(election_id)
#        return jsonify({
#            'election_id': election_id,
#            'results': results
#        }), 200
#    except Exception as e:
#        print(f"Error during result tallying: {e}")
#        return jsonify({'error': 'Internal Server Error'}), 500
