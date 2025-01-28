import pytest
from app import app, db
from models import Election
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


# get all elections checkes 
def test_get_elections(test_client):
    tmp1 = Election(title="tmp1 election", status="Open")
    tmp2 = Election(title="tmp2 election", status="Open")
    db.session.add(tmp1)
    db.session.add(tmp2)
    db.session.commit()

    response = helper_register_user(test_client, 'peppe', 'pass')
    response, access_token = helper_login_user(test_client, 'peppe', 'pass')
    access_headers = {"Authorization": "Bearer {}".format(access_token)}

    response = test_client.get('/api/elections/get_elections', headers=access_headers)

    print(f"token : {access_token}")
    print(f"response : {response.get_json()}")

    assert response.status_code == 200
    elections = response.get_json()
    assert len(elections) == 2
    assert elections[0]['title'] == 'tmp1 election'
    assert elections[1]['title'] == 'tmp2 election'


#def test_create_election(test_client):
#    user, password, role, key  = 'peppe', '12345', 'admin','default_admin_key' 
#    
#    response = helper_register_user(test_client, user, password, role, key)
#    assert response.status_code == 201
#
#    response, token = helper_login_user(test_client, user, password)
#    assert response.status_code == 200
#
#    response = test_client.post(
#        '/api/elections/create_election', 
#        json = {
#        'title': 'Presidential Election 2025'
#        },
#        headers = {
#        'Authorization': f'Bearer {token}'
#        }
#    )
#    assert response.status_code == 201
#    #assert response.get_json()['message'] == 'Election created successfully'



#def test_create_election_with_no_permission(test_client):
#    voter_token = login_user(test_client, 'voter', 'voter123')
#    response = test_client.post('/api/elections/', json={
#        'title': 'Unauthorized Election'
#    }, headers={
#        'Authorization': f'Bearer {voter_token}'
#    })
#    assert response.status_code == 403
#    assert response.get_json()['error'] == 'Unauthorized'


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
