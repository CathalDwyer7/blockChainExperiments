# pytest -s -p no:warnings 
import pytest
from datetime import datetime, timedelta

from models import Election
from app import app, db
from typing import Optional
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
