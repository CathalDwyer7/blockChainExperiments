from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from models import Election, Candidates
from extensions import db
from .auth import admin_required

election_routes = Blueprint("elections", __name__)


@election_routes.route("/get_elections", methods=["GET"])
@jwt_required()
def get_elections():
    elections = Election.query.all()
    data = []
    for election in elections:
        candidates = Candidates.query.filter_by(election_id=election.id).all()
        data.append(
            {
                "id": election.id,
                "title": election.title,
                "start_credits": election.start_credits,
                "start_date": election.start_date,
                "end_date": election.end_date,
                "description": election.description,
                "status": election.status.value,
                "candidates": [
                    {
                        "id": candidat.id,
                        "name": candidat.name,
                        "description": candidat.description,
                    }
                    for candidat in candidates
                ],
            }
        )

    return jsonify(data), 200


@election_routes.route("/get_election/<int:id>", methods=["GET"])
@jwt_required()
def get_election_by_id(id):
    election = Election.query.get(id)

    if election is None:
        return jsonify({"error": "Election not found"}), 404

    candidates = Candidates.query.filter_by(election_id=election.id).all()

    data = {
        "id": election.id,
        "title": election.title,
        "start_credits": election.start_credits,
        "start_date": election.start_date,
        "end_date": election.end_date,
        "description": election.description,
        "status": election.status.value,
        "candidates": [
            {
                "id": candidate.id,
                "name": candidate.name,
                "description": candidate.description,
            }
            for candidate in candidates
        ],
    }
    return jsonify(data), 200




@election_routes.route("/create_election", methods=["POST"])
@admin_required
def create_election():
    data = request.get_json()

    required_fields = [
        "title",
        "start_credits",
        "start_date",
        "end_date",
        "description",
    ]
    missing_fields = [filed for filed in required_fields if filed not in data]

    if missing_fields:
        return jsonify({"error": f'{", ".join(missing_fields)} are required'}), 400

    new_election = Election(
        title=data.get("title"),
        start_credits=int(data.get("start_credits")),
        start_date=int(data.get("start_date")),
        end_date=int(data.get("end_date")),
        description=data.get("description"),
    )

    db.session.add(new_election)
    db.session.commit()

    if "candidates" in data:
        for c in data["candidates"]:
            new_candidate = Candidates(
                election_id=new_election.id,
                name=c["name"],
                description=c.get("description", ""),
            )
            db.session.add(new_candidate)
        db.session.commit()

    candidates = Candidates.query.filter_by(election_id=new_election.id).all()

    output_data = {
        "id": new_election.id,
        "title": new_election.title,
        "start_credits": new_election.start_credits,
        "start_date": new_election.start_date,
        "end_date": new_election.end_date,
        "description": new_election.description,
        "candidates": [
            {"id": c.id, "name": c.name, "description": c.description}
            for c in candidates
        ],
    }
    return jsonify(output_data), 201
