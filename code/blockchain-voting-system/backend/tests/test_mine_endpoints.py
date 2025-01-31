import pytest
import hashlib
from app import app, db
from .test_election_endpoints import helper_get_user_headers

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

def test_get_mining_data(test_client):
    response = test_client.get(
        '/api/mine/info', 
        headers=helper_get_user_headers(test_client)
    )

    data = response.get_json()

    assert response.status_code == 200
    assert 'last_proof' in data
    assert 'difficulty' in data

def helper_mine_a_block(last_proof, POW_DIFFICULTY):
    def is_valid_pow(last_pow: int, new_pow: int) -> bool:
        guess = f"{last_pow}{new_pow}".encode()
        hashed_guess = hashlib.sha256(guess).hexdigest()
        return hashed_guess[:POW_DIFFICULTY] == "0" * POW_DIFFICULTY

    def proof_of_work(last_proof: int) -> int:
        new_proof = 0
        while not is_valid_pow(last_proof, new_proof):
            new_proof += 1
        return new_proof
    
    return proof_of_work(last_proof) 

def test_mine(test_client):
    access_headers = helper_get_user_headers(test_client)
    response = test_client.get('/api/mine/info', headers=access_headers)
    data = response.get_json()
    last_pof, diff =  data['last_proof'], data['difficulty']
    new_proof = helper_mine_a_block(last_pof, diff)

    response = test_client.post('/api/mine/mine-block', json={'proof': new_proof}, headers=access_headers)
    data = response.get_json()

    assert response.status_code == 201
    assert data['msg'] == 'New block mined!'
