import pytest
from app import app, db
from models import User
from werkzeug.security import generate_password_hash

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

@pytest.fixture
def setup_data(client):
    with app.app_context():
        # Add an admin user
        admin = User(username='admin', password=generate_password_hash('admin123'), role='admin', credits=0)
        voter = User(username='voter',password=generate_password_hash('voter123'), role='voter', credits=100)
        db.session.add(admin)
        db.session.add(voter)
        db.session.commit()

# Helper function to log in and return a JWT token
def login(client, username, password):
    response = client.post('/api/auth/login', json={
        'username': username,
        'password': password
    })
    return response.json.get('access_token')

def test_full_election_flow(client, setup_data):
    # 1. Admin logs in
    admin_token = login(client, 'admin', 'admin123')
    assert admin_token is not None

    # 2. Create an election
    response = client.post('/api/elections/',
                           json={'title': 'Test Election'},
                           headers={'Authorization': f'Bearer {admin_token}'}
                           )
    assert response.status_code == 201
    election_id = response.json['id']

    # 3. Admin marks the election as Ongoing
    response = client.patch(f'/api/elections/{election_id}/status',
                            json={'status': 'Ongoing'},
                            headers={'Authorization': f'Bearer {admin_token}'}
                            )
    assert response.status_code == 200

    # 4. Voter logs in
    voter_token = login(client, 'voter', 'voter123')
    assert voter_token is not None

    # 5. Voter casts votes
    response = client.post('/api/elections/vote',
                           json={
                               'election_id': election_id,
                               'votes': 3,
                               'proposal': 'Candidate A'
                           },
                           headers={'Authorization': f'Bearer {voter_token}'}
                           )
    assert response.status_code == 201

    # 6. Admin ends the election
    response = client.patch(f'/api/elections/{election_id}/status',
                            json={'status': 'Completed'},
                            headers={'Authorization': f'Bearer {admin_token}'}
                            )
    assert response.status_code == 200

    # 7. Fetch results
    response = client.get(f'/api/elections/results/{election_id}')
    assert response.status_code == 200
    results = response.json['results']
    assert results == {'Candidate A': 3}
