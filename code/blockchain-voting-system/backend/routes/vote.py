from .__init__ import block_chain
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Election, User, Candidates, ElectionCredits, ElectionStatus
from extensions import db
from block_chain.encryption.paillier import encrypt, decrypt
from typing import Optional

vote_routes = Blueprint("vote", __name__)

@vote_routes.route("/public_key_election/<int:id>", methods=["GET"])
@jwt_required()
def get_election_public_key(id):
    election = Election.query.get(id)

    if election is None:
        return jsonify({"error": "Election not found"}), 404

    return jsonify({'public_key':election.public_key}), 200


@vote_routes.route("/private_key_election/<int:id>", methods=["GET"])
@jwt_required()
def get_election_private_key(id):
    election = Election.query.get(id)

    if election is None:
        return jsonify({"error": "Election not found"}), 404

    #uncomment after testing
    #from models import ElectionStatus

    #if election.status != ElectionStatus.COMPLETED:
    #    return jsonify({"error": "It is not possible to get the private key before the election is completed"}), 400

    return jsonify({'private_key':election.private_key}), 200

@vote_routes.route("/election_credits_left/<int:id>", methods=["GET"])
@jwt_required()
def get_election_credits_left(id):
    current_user = get_jwt_identity()
    user: Optional[User] = User.query.get(current_user['id'])
    election: Optional[Election] = Election.query.get(id)

    if election is None or user is None:
        return jsonify({"error": "Election or User not found"}), 404

    election_credit = ElectionCredits.query.filter_by(
        user_id=user.id, election_id=election.id
    ).first()

    user_public_key = user.public_key['n'], user.public_key['g'] 

    if not election_credit:
        election_credit = ElectionCredits(
            user_id=user.id,
            election_id=election.id,
            credits_left=encrypt(election.start_credits, user_public_key)
        )
        db.session.add(election_credit)
    
    return jsonify({'encrypted_credits_left':election_credit.credits_left}), 200

@vote_routes.route("/submit", methods=["POST"])
@jwt_required()
def vote_election_by_id():
    data = request.get_json()
    current_user = get_jwt_identity()

    required_fields = [
        "election_id", 
        "encrypted_candidate_id", 
        "encrypted_votes", 
        "encrypted_cost",
        "candidate_commitment",
        "votes_commitment",
        "cost_commitment",
        "zkp_proofs"
    ]

    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({"error": f'{", ".join(missing_fields)} are required'}), 400
    
    user: Optional[User] = User.query.get(current_user['id']) 
    election: Optional[Election] = Election.query.get(data['election_id'])

    if not election:
        return jsonify({"error": "Election not found"}), 404

    if election.status != ElectionStatus.ONGOING:
        return jsonify({"error": "Election is not active"}), 400

    # Check Pedersen Commitments
    

