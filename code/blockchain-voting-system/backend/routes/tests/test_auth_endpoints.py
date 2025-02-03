import pytest
from app import app, db
from models import User

@pytest.fixture(scope="function")
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            yield testing_client
            db.session.remove()
            db.drop_all()


# database and cleaning between each test checkes 
def test_data_base_integrity(test_client):
    tmp_record = User(username='peppe',password='ciaociao')
    db.session.add(tmp_record)
    db.session.commit()
    assert User.query.count() == 1

def test_data_base_cleaning(test_client):
    assert User.query.count() == 0


# "/register" endpoint checkes
def helper_register_user(client, username, password, key=''):
    if len(key) > 0:
        return client.post('/api/auth/register', json={
            'username': username,
            'password': password,
            'key': key,
        })

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
    response = helper_register_user(test_client, 'peppe', 'bho', 'default_admin_key')
    assert response.status_code == 201
    assert response.get_json()['message'] == 'User registered successfully'

def test_register_admin_wrong_key(test_client):
    response = helper_register_user(test_client, 'peppe', 'bho', 'random_key')
    assert response.status_code == 400 
    assert response.get_json()['error'] == 'Error the admin key is incorrect'


#  "/login" endpoint checkes 
def helper_login_user(client, username, password):
    response = client.post('/api/auth/login', json={
        'username': username,
        'password': password
    })
    token = response.get_json()['access_token'] if response.status_code == 200 else None
    return response, token

def test_login_user(test_client):
    helper_register_user(test_client, 'voter', 'voter123')
    response, _ = helper_login_user(test_client, 'voter', 'voter123')
    assert response.status_code == 200
    assert 'access_token' in response.get_json()

def test_login_user_wrong_password(test_client):
    helper_register_user(test_client, 'voter', 'voter123', 'voter')
    response, _ = helper_login_user(test_client, 'voter', 'wrongpass')
    assert response.status_code == 401
    assert response.get_json()['error'] == 'Invalid credentials'

#  "/protected" endpoint checks to test jwt decortor
def test_protected_endpoint(test_client):
    _ = helper_register_user(test_client, 'peppe', '12345')
    _, access_token = helper_login_user(test_client, 'peppe', '12345')
    access_headers = {"Authorization": "Bearer {}".format(access_token)} 
    response = test_client.get('api/auth/protected', headers=access_headers)
    assert response.status_code == 200
    print(response.get_json())

def test_protected_endpoint_no_token(test_client):
    response = test_client.get('api/auth/protected')
    assert response.status_code == 401 
    assert response.get_json()['msg'] == 'Missing Authorization Header'


def test_protected_endpoint_fake_token(test_client):
    fake_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEyMzQ1Iiwicm9sZSI6ImFkbWluIiwiaWF0IjoxNjc3MDAwMDAwLCJleHAiOjE2NzcwMzYwMDB9.VP9l65bWbUj9QFsuqZTUbGFd5wVk3TA5-QeRlsuTQ6Y"
    access_headers = {"Authorization": "Bearer {}".format(fake_token)} 
    response = test_client.get('api/auth/protected', headers=access_headers)
    assert response.status_code == 422
    assert response.get_json()['msg'] == "Signature verification failed"
