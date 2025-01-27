import pytest
from app import app, db
from models import Election

# Configure a test database
TEST_DATABASE_URI = 'sqlite:///test_db.sqlite'

@pytest.fixture(scope="function")
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            yield testing_client
            db.session.remove()
            db.drop_all()

# data base and cleaning between each test checkes 
def test_data_base_integrity(test_client):
    tmp_record = Election(title="tmp election", status="Open")
    db.session.add(tmp_record)
    db.session.commit()
    assert Election.query.count() == 1

def test_data_base_cleaning(test_client):
    assert Election.query.count() == 0


# "/register" endpoint checkes
def helper_register_user(client, username, password, role='', key=''):
    if len(role) > 0 and len(key) > 0:
        return client.post('/api/auth/register', json={
            'username': username,
            'password': password,
            'role': role,
            'key': key,
        })
    else:
        return client.post('/api/auth/register', json={
            'username': username,
            'password': password,
        })

def test_register_user(test_client):
    response = helper_register_user(test_client, 'peppe', 'bho')
    assert response.status_code == 201
    assert response.get_json()['message'] == 'User registered successfully'

def test_register_user_same_username(test_client):
    _ = helper_register_user(test_client, 'peppe', 'bho')
    response = helper_register_user(test_client, 'peppe', 'bho')

    assert response.status_code == 400
    assert response.get_json()['error'] == 'Username already exists'

def test_register_admin(test_client):
    response = helper_register_user(test_client, 'peppe', 'bho', 'admin', 'default_admin_key')
    assert response.status_code == 201
    assert response.get_json()['message'] == 'User registered successfully'

def test_register_admin_wrong_key(test_client):
    response = helper_register_user(test_client, 'peppe', 'bho', 'admin', 'random_key')
    assert response.status_code == 400 
    assert response.get_json()['error'] == 'Error the admin key is incorrect'

## "/login" endpoint checkes 
def helper_login_user(client, username, password):
    response = client.post('/api/auth/login', json={
        'username': username,
        'password': password
    })
    token = response.get_json()['access_token'] if response.status_code == 200 else None
    return response, token

def test_login_user(test_client):
    helper_register_user(test_client, 'voter', 'voter123', 'voter')
    response, _ = helper_login_user(test_client, 'voter', 'voter123')
    assert response.status_code == 200
    assert 'access_token' in response.get_json()

def test_login_user_wrong_password(test_client):
    helper_register_user(test_client, 'voter', 'voter123', 'voter')
    response, _ = helper_login_user(test_client, 'voter', 'wrongpass')
    assert response.status_code == 401
    assert response.get_json()['error'] == 'Invalid credentials'

#def test_create_election(test_client):
#    admin_token = login_user(test_client, 'admin', 'admin123')
#
#    # Admin creates an election
#    response = test_client.post('/api/elections/', json={
#        'title': 'Presidential Election 2025'
#    }, headers={
#        'Authorization': f'Bearer {admin_token}'
#    })
#    assert response.status_code == 201
#    assert response.get_json()['message'] == 'Election created successfully'
#
#    # Voter tries to create an election
#    voter_token = login_user(test_client, 'voter', 'voter123')
#    response = test_client.post('/api/elections/', json={
#        'title': 'Unauthorized Election'
#    }, headers={
#        'Authorization': f'Bearer {voter_token}'
#    })
#    assert response.status_code == 403
#    assert response.get_json()['error'] == 'Unauthorized'
#
#def test_get_elections(test_client):
#    response = test_client.get('/api/elections/')
#    assert response.status_code == 200
#    elections = response.get_json()
#    assert len(elections) == 1
#    assert elections[0]['title'] == 'Presidential Election 2025'
#
#def test_submit_vote(test_client):
#    voter_token = login_user(test_client, 'voter', 'voter123')
#
#    # Voter submits a vote
#    response = test_client.post('/api/elections/vote', json={
#        'election_id': 1,
#        'proposal': 'Proposal A',
#        'votes': 4
#    }, headers={
#        'Authorization': f'Bearer {voter_token}'
#    })
#    assert response.status_code == 201
#    assert response.get_json()['message'] == 'Vote submitted successfully'
#
#    # Voting for a non-existent election
#    response = test_client.post('/api/elections/vote', json={
#        'election_id': 999,
#        'proposal': 'Nonexistent Proposal',
#        'votes': 1
#    }, headers={
#        'Authorization': f'Bearer {voter_token}'
#    })
#    assert response.status_code == 404
#    assert response.get_json()['error'] == 'Election not found'
