from flask import Blueprint, jsonify, request

election_routes = Blueprint('elections', __name__)

# Mock election data
elections = [
    {'id': 1, 'title': 'Presidential Election 2024', 'status': 'Ongoing'},
    {'id': 2, 'title': 'City Council Election', 'status': 'Ended'}
]

@election_routes.route('/', methods=['GET'])
def get_elections():
    return jsonify(elections)

@election_routes.route('/', methods=['POST'])
def create_election():
    data = request.get_json()
    new_election = {
        'id': len(elections) + 1,
        'title': data.get('title'),
        'status': 'Upcoming'
    }
    elections.append(new_election)
    return jsonify(new_election), 201
