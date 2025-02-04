# pytest -s -p no:warnings routes/tests/test_election_endpoints.py
# run with this command bc datetime.utc is deprecated and we need to change it later
from datetime import datetime, timedelta
import pytest

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import Election, Candidates
from .test_auth_endpoints import helper_login_user, helper_register_user

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


def helper_create_election():
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

    cand1 = Candidates(election_id=tmp.id, name='cand1', description='desc1')
    cand2 = Candidates(election_id=tmp.id, name='cand2', description='desc2')

    db.session.add_all([cand1,cand2])
    db.session.commit()
    return tmp.id

def helper_get_user_headers(test_client):
    _ = helper_register_user(test_client, 'peppe', 'pass')
    _, access_token = helper_login_user(test_client, 'peppe', 'pass')
    return {"Authorization": "Bearer {}".format(access_token)}

def helper_get_admin_headers(test_client):
    _ = helper_register_user(test_client, 'peppe', 'pass','default_admin_key')
    _, access_token = helper_login_user(test_client, 'peppe', 'pass')
    return {"Authorization": "Bearer {}".format(access_token)}

# get all elections checkes 
def test_get_elections(test_client):
    helper_create_election()
    access_headers = helper_get_user_headers(test_client)
    response = test_client.get('/api/elections/get_elections', headers=access_headers)
    assert response.status_code == 200
    elections = response.get_json()
    assert len(elections) == 1
    assert elections[0]['title'] == 'Something'



def test_create_election(test_client):
    access_headers = helper_get_admin_headers(test_client)
    endpoint = '/api/elections/create_election'
    start_unix = int(datetime.utcnow().timestamp())
    end_unix = int((datetime.utcnow() + timedelta(hours=2)).timestamp())
    data = {
        'title':"Something", 
        'start_credits':10, 
        'start_date':start_unix,
        'end_date':end_unix,
        'description':"Some kind of election",
    }

    response = test_client.post(endpoint, json=data, headers=access_headers)
    assert response.status_code == 201

def test_create_election_with_no_permission(test_client):
    access_headers = helper_get_user_headers(test_client)
    endpoint = '/api/elections/create_election'
    start_unix = int(datetime.utcnow().timestamp())
    end_unix = int((datetime.utcnow() + timedelta(hours=2)).timestamp())
    data = {
        'title':"Something", 
        'start_credits':10, 
        'start_date':start_unix,
        'end_date':end_unix,
        'description':"Some kind of election",
    }

    response = test_client.post(endpoint, json=data, headers=access_headers)
    assert response.status_code == 403

def test_create_election_with_candidates(test_client):
    access_headers = helper_get_admin_headers(test_client)
    endpoint = '/api/elections/create_election'
    start_unix = int(datetime.utcnow().timestamp())
    end_unix = int((datetime.utcnow() + timedelta(hours=2)).timestamp())
    data = {
        'title':"Something", 
        'start_credits':10, 
        'start_date':start_unix,
        'end_date':end_unix,
        'description':"Some kind of election",
        'candidates': [
            {'name':'mario', 'description': 'left guy'},
            {'name':'cesare', 'description': 'right guy'}
        ]
    }

    response = test_client.post(endpoint, json=data, headers=access_headers)
    assert response.status_code == 201


def test_get_election_by_id(test_client):
    id = helper_create_election()
    _ = helper_create_election()
    access_headers = helper_get_user_headers(test_client)

    response = test_client.get(f'/api/elections/get_election/{id}', headers=access_headers)
    assert response.status_code == 200
    assert response.get_json()['id'] == id
