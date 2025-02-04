from .__init__ import block_chain
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Election, User, Candidates, ElectionCredits, ElectionStatus
from extensions import db

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


#@vote_routes.route("/submit", methods=["POST"])
#@jwt_required()
#def vote_election_by_id():
#    data = request.get_json()
#    current_user = get_jwt_identity()
#
#    required_fields = ["election_id", "candidate_id", "votes"]
#    missing_fields = [field for field in required_fields if field not in data]
#
#    if missing_fields:
#        return jsonify({"error": f'{", ".join(missing_fields)} are required'}), 400
#
#    try:
#        user = User.query.get(int(current_user["id"]))
#        election = Election.query.get(int(data["election_id"]))
#        candidate = Candidates.query.get(int(data["candidate_id"]))
#        votes = int(data["votes"])
#    except (ValueError, TypeError) as e:
#        return jsonify({"error": f"Invalid data: {str(e)}"}), 400
#
#    if (not user) or (not election) or (not candidate):
#        return jsonify({"error": "User, election, or candidate does not exist"}), 400
#
#    if candidate.election_id != election.id:
#        return  jsonify({"error": f"{candidate.name} is not a candidate in the election: {election.title}"}), 400
#
#    if election.status != ElectionStatus.ONGOING:
#        return jsonify({"error": "It is not possible to vote in this election"}), 400
#
#    if votes <= 0:
#        return jsonify({"error": "Votes must be a positive integer"}), 400
#
#    election_credit = ElectionCredits.query.filter_by(
#        user_id=user.id, election_id=election.id
#    ).first()
#
#    if not election_credit:
#        election_credit = ElectionCredits(
#            user_id=user.id,
#            election_id=election.id,
#            credits_left=election.start_credits,
#        )
#        db.session.add(election_credit)
#
#    cost = votes**2
#
#    if cost > election_credit.credits_left:
#        return jsonify({"error": "You don't have enough credits"}), 400
#
#    election_credit.credits_left -= cost
#    db.session.commit()
#
#    try:
#        block_chain.new_vote(
#            user_id=user.id,
#            election_id=election.id,
#            candidate_id=candidate.id,
#            votes=votes,
#        )
#    except Exception as e:
#        db.session.rollback()
#        return jsonify({"error": f"Blockchain error: {str(e)}"}), 500
#
#    return jsonify({"message": "Vote submitted successfully"}), 201
