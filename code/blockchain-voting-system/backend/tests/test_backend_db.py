import pytest
from app import app, db
from models import User, Election

# Configure a test database
TEST_DATABASE_URI = 'sqlite:///test_db.sqlite'

@pytest.fixture(scope="module")
def test_client():
    # Set up the Flask app for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Create the test client
    with app.test_client() as testing_client:
        with app.app_context():
            # Initialize the database
            db.create_all()
            yield testing_client
            db.drop_all()

# Helper function to register a user
def register_user(client, username, password, role):
    return client.post('/api/auth/register', json={
        'username': username,
        'password': password,
        'role': role
    })

# Helper function to log in a user
def login_user(client, username, password):
    response = client.post('/api/auth/login', json={
        'username': username,
        'password': password
    })
    return response.get_json()['access_token'] if response.status_code == 200 else None

def test_register_user(test_client):
    response = register_user(test_client, 'admin', 'admin123', 'admin')
    assert response.status_code == 201
    assert response.get_json()['message'] == 'User registered successfully'

    response = register_user(test_client, 'admin', 'admin123', 'admin')
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Username already exists'

def test_login_user(test_client):
    register_user(test_client, 'voter', 'voter123', 'voter')

    response = test_client.post('/api/auth/login', json={
        'username': 'voter',
        'password': 'voter123'
    })
    assert response.status_code == 200
    assert 'access_token' in response.get_json()

    response = test_client.post('/api/auth/login', json={
        'username': 'voter',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert response.get_json()['error'] == 'Invalid credentials'

def test_create_election(test_client):
    admin_token = login_user(test_client, 'admin', 'admin123')

    # Admin creates an election
    response = test_client.post('/api/elections/', json={
        'title': 'Presidential Election 2025'
    }, headers={
        'Authorization': f'Bearer {admin_token}'
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Election created successfully'

    # Voter tries to create an election
    voter_token = login_user(test_client, 'voter', 'voter123')
    response = test_client.post('/api/elections/', json={
        'title': 'Unauthorized Election'
    }, headers={
        'Authorization': f'Bearer {voter_token}'
    })
    assert response.status_code == 403
    assert response.get_json()['error'] == 'Unauthorized'

def test_get_elections(test_client):
    response = test_client.get('/api/elections/')
    assert response.status_code == 200
    elections = response.get_json()
    assert len(elections) == 1
    assert elections[0]['title'] == 'Presidential Election 2025'

def test_submit_vote(test_client):
    voter_token = login_user(test_client, 'voter', 'voter123')

    # Voter submits a vote
    response = test_client.post('/api/elections/vote', json={
        'election_id': 1,
        'proposal': 'Proposal A',
        'votes': 4
    }, headers={
        'Authorization': f'Bearer {voter_token}'
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Vote submitted successfully'

    # Voting for a non-existent election
    response = test_client.post('/api/elections/vote', json={
        'election_id': 999,
        'proposal': 'Nonexistent Proposal',
        'votes': 1
    }, headers={
        'Authorization': f'Bearer {voter_token}'
    })
    assert response.status_code == 404
    assert response.get_json()['error'] == 'Election not found'
