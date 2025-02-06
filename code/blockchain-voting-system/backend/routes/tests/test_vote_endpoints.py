# pytest -s -p no:warnings 
import pytest
from datetime import datetime, timedelta

from models import Election, Candidates
from app import app, db
from typing import Optional
from .test_election_endpoints import helper_get_user_headers
from block_chain.encryption.paillier import encrypt, decrypt, generate_paillier_keypair

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

def heleper_add_election_get_keys():
    start_unix = int(datetime.utcnow().timestamp())
    end_unix = int((datetime.utcnow() + timedelta(hours=2)).timestamp())

    tmp = Election(
        title="Something", 
        start_credits=10, 
        start_date=start_unix,
        end_date=end_unix,
        description="Some kind of election",
    )
    db.session.add(tmp)
    db.session.commit()

    tmp: Optional[Election] = Election.query.get(tmp.id)
    
    if tmp is None:
        return exit(0) 

    # public
    n = tmp.public_key.get('n')
    g = tmp.public_key.get('g')

    # private
    lambda_val = tmp.private_key.get('lambda')
    mu = tmp.private_key.get('mu')
    p = tmp.private_key.get('p')

    assert n == p 

    return (n,g) , (lambda_val, mu, p) , tmp.id

def test_get_keys_endpoint(test_client):
    (n, g), (lambda_val , mu, p), election_id = heleper_add_election_get_keys()

    response = test_client.get(
        f'/api/vote/public_key_election/{election_id}',
        headers=helper_get_user_headers(test_client)
    )

    # public key test
    assert response.get_json()['public_key']['n'] == n
    assert response.get_json()['public_key']['g'] == g
    
    response = test_client.get(
        f'/api/vote/private_key_election/{election_id}',
        headers=helper_get_user_headers(test_client)
    )

    # private key test
    assert response.get_json()['private_key']['lambda'] == lambda_val
    assert response.get_json()['private_key']['mu'] == mu 
    assert response.get_json()['private_key']['p'] == p 

def test_submit_vote_endpoint(test_client):
    # ====================================================
    # 0. create an election:
    # ====================================================

    start_unix = int(datetime.utcnow().timestamp())
    end_unix = int((datetime.utcnow() + timedelta(hours=2)).timestamp())

    election_target = Election(
        title="Secure Election with paillier", 
        start_credits=10, 
        start_date=start_unix,
        end_date=end_unix,
        description="Secure election",
    )
    db.session.add(election_target)
    db.session.commit()

    cand1 = Candidates(election_id=election_target.id, name='cand1', description='desc1')
    cand2 = Candidates(election_id=election_target.id, name='cand2', description='desc2')

    db.session.add_all([cand1,cand2])
    db.session.commit()

    # ====================================================
    # 1. create a user and login:
    # ====================================================

    # 1.1 user genereate keys to encypt his credit_lefts
    USER, PASS = 'peppe', '12345'

    # 1.2 user register with username, password and public_keys
    resp = test_client.post('/api/auth/register', json={
        'username': USER,
        'password': PASS,
    })
    assert resp.status_code == 201

    # 1.3 then the user login and get is access token
    response = test_client.post('/api/auth/login', json={
        'username': USER,
        'password': PASS 
    })

    token = response.get_json()['access_token']
    access_headers = {"Authorization": "Bearer {}".format(token)}
    
    # ====================================================
    # 2. the user want to cast 2 votes for the candidate 1
    # ====================================================

    # 2.1 first fetch the public_key for this election
    response = test_client.get(
        f'/api/vote/public_key_election/{election_target.id}',
        headers=access_headers
    )
    json = response.get_json()

    election_pb_key = int(json['public_key']['n']), int(json['public_key']['g'])

    # 2.2 fetch how many credits he has left in this election 

    response = test_client.get(
        f'/api/vote/election_credits_left/{election_target.id}',
        headers=access_headers
    )

    json = response.get_json()
    credits_left = int(json['credits_left'])
    assert credits_left == 10

    # 2.3 create the payload to send to the /submit endpoint

    pay_load = {
        "election_id":election_target.id, 
        "encrypted_candidate_id":encrypt(int(cand1.id), election_pb_key), 
        "votes": 2
    }
    
    response = test_client.post(
        '/api/vote/submit',
        json=pay_load,
        headers=access_headers
    )

    assert response.status_code == 200 

    # 2.3 after we use 2 votes we spent 2 ** 2 = 4 credits
    # our credits now should be 10 - 4 = 6
    
    response = test_client.get(
        f'/api/vote/election_credits_left/{election_target.id}',
        headers=access_headers
    )

    json = response.get_json()
    credits_left = int(json['credits_left'])
    assert credits_left == 6 

    # 2.4 let's try to cast 6 vote that we can not afford

    pay_load = {
        "election_id":election_target.id, 
        "encrypted_candidate_id":encrypt(int(cand2.id), election_pb_key), 
        "votes": 6
    }
    
    response = test_client.post(
        '/api/vote/submit',
        json=pay_load,
        headers=access_headers
    )

    assert response.status_code == 400 
    assert response.get_json()['error'] == f"You do not have enough credtis to cast {6} votes"
    # our credits should be still 6
    response = test_client.get(
        f'/api/vote/election_credits_left/{election_target.id}',
        headers=access_headers
    )

    json = response.get_json()
    credits_left = int(json['credits_left'])
    assert credits_left == 6 

    # 3 Check the results
    
    # 3.1 mine a block to save the votes
    import hashlib
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

    response = test_client.get('/api/mine/info', headers=access_headers)
    data = response.get_json()
    last_pof, diff =  data['last_proof'], data['difficulty']
    new_proof = helper_mine_a_block(last_pof, diff)

    response = test_client.post('/api/mine/mine-block', json={'proof': new_proof}, headers=access_headers)
    data = response.get_json()

    assert response.status_code == 201
    assert data['msg'] == 'New block mined!'

    # 3.2 fetch the results
    response = test_client.get(
        f'/api/vote/result/{election_target.id}',
        headers=access_headers
    )

    print(response.get_json())




    

