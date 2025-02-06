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


    if not election_credit:
        election_credit = ElectionCredits(
            user_id=user.id,
            election_id=election.id,
            credits_left=election.start_credits
        )
        db.session.add(election_credit)
        db.session.commit()
    
    return jsonify({'credits_left':election_credit.credits_left}), 200

@vote_routes.route("/submit", methods=["POST"])
@jwt_required()
def vote_election_by_id():
    data = request.get_json()
    current_user = get_jwt_identity()

    required_fields = [
        "election_id", 
        "encrypted_candidate_id", 
        "votes"
    ]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f'{", ".join(missing_fields)} are required'}), 400
    
    try:
        user_id = current_user['id']
        election_id = int(data['election_id'])
        en_candidate_id = int(data['encrypted_candidate_id'])
        votes = int(data['votes'])
        cost = votes ** 2
    except ValueError:
        return jsonify({"error": "election_id,encrypted_candidate_id, and votes must be int "}), 400


    user: Optional[User] = User.query.get(user_id) 
    election: Optional[Election] = Election.query.get(election_id)

    if not election or not user:
        return jsonify({"error": "Election not found"}), 404

    if election.status != ElectionStatus.ONGOING:
        return jsonify({"error": "Election is not active"}), 400

    election_credit = ElectionCredits.query.filter_by(
        user_id=user.id, election_id=election.id
    ).first()

    if not election_credit:
        election_credit = ElectionCredits(
            user_id=user.id,
            election_id=election.id,
            credits_left=election.start_credits
        )
        db.session.add(election_credit)
        db.session.commit()
        
    if election_credit.credits_left < cost:
        return jsonify({"error": f"You do not have enough credtis to cast {votes} votes"}), 400

    election_credit.credits_left -= cost
    db.session.commit()

    election_key = int(election.public_key['n']), int(election.public_key['g'])
    block_chain.new_vote(election_id, en_candidate_id, encrypt(votes, election_key))

    return jsonify({"msg": "You have submitted your vote correctly"}), 200 


