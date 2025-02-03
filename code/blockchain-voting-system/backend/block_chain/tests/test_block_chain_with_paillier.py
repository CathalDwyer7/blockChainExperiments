import hashlib
import pytest

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chain import Chain
from typing import List
from vote import Vote

from encryption.paillier import (
    decrypt_string,
    encrypt_string,
    generate_paillier_keypair,
    encrypt,
    decrypt,
)

@pytest.fixture
def blockchain():
    """ Create a blockchain obj """
    return Chain()

@pytest.fixture
def paillier_keys():
    """ Generate a private and publick key with paillier """
    public_key, private_key = generate_paillier_keypair(key_size=256)
    return public_key, private_key

def test_hashing_block(blockchain: Chain):
    block = blockchain.last_block
    block_hash = blockchain.hash(block)

    assert isinstance(block_hash, str)
    assert len(block_hash) == 64  
    assert all(c in "0123456789abcdef" for c in block_hash)

def test_block_as_dict(blockchain: Chain, paillier_keys):
    public_key, _ = paillier_keys
    election_id = 1
    candidate_id = 42 
    votes = 5

    en_candidate_id = encrypt(candidate_id, public_key)
    en_votes = encrypt(votes, public_key)

    blockchain.new_vote(
        election_id,
        en_candidate_id,
        en_votes ,
    )
    
    proof = blockchain.proof_of_work(blockchain.last_block.proof)
    new_block = blockchain.new_block(proof)

    block_dict = new_block.as_dict()
    votes = block_dict['votes']

    assert isinstance(block_dict, dict)
    assert block_dict["index"] == new_block.index
    assert block_dict["proof"] == new_block.proof
    assert block_dict["previous_hash"] == new_block.previous_hash
    assert len(votes) == 1
    assert votes[0]['election_id'] == election_id
    assert votes[0]['encrypted_candidate_id'] == en_candidate_id
    assert votes[0]['encrypted_votes'] == en_votes 



def test_genesis_block(blockchain: Chain):
    """ Check if the first block is the genesis one """
    assert len(blockchain.blocks) == 1
    genesis = blockchain.last_block
    assert genesis.proof == 10
    assert genesis.previous_hash == "1"

def test_add_vote(blockchain: Chain, paillier_keys):
    public_key, private_key = paillier_keys
    election_id = 1
    candidate_id = 42 
    votes = 5

    en_cand_id = encrypt(candidate_id, public_key) 
    en_votes = encrypt(votes, public_key)

    idx = blockchain.new_vote(election_id, en_cand_id, en_votes)
    
    assert idx == blockchain.last_block.index + 1
    assert len(blockchain.current_votes) == 1

    vote = blockchain.current_votes[0]
    assert vote.election_id == 1 
    assert vote.encrypted_candidate_id == en_cand_id 
    assert vote.encrypted_votes == en_votes 
    assert decrypt(vote.encrypted_candidate_id, private_key) == candidate_id
    assert decrypt(vote.encrypted_votes, private_key) == votes

def test_proof_of_work(blockchain: Chain):
    last_proof = blockchain.last_block.proof
    new_proof = blockchain.proof_of_work(last_proof)

    guess = f"{last_proof}{new_proof}".encode()
    hashed_guess = hashlib.sha256(guess).hexdigest()

    assert hashed_guess[:blockchain.POW_DIFFICULTY] == "0" * blockchain.POW_DIFFICULTY

def test_mine_block(blockchain: Chain, paillier_keys):
    public_key, _ = paillier_keys
    election_id = 1
    candidate_id = 42 
    votes = 5

    blockchain.new_vote(
        election_id,
        encrypt(candidate_id, public_key),
        encrypt(votes, public_key)
    )
   
    last_proof = blockchain.last_block.proof
    proof = blockchain.proof_of_work(last_proof)
    new_block = blockchain.new_block(proof)
    
    assert len(blockchain.blocks) == 2
    assert new_block.index == 2

    expected_prev_hash = blockchain.hash(blockchain.blocks[-2])
    assert new_block.previous_hash == expected_prev_hash

    assert blockchain.last_block.votes[0].election_id == election_id

def test_vote_counter(blockchain: Chain):
    public_key_1, private_key_1 = generate_paillier_keypair(key_size=256)

    election_1 = {
        'id': 1,
        'candidates': [
            {
                'id': 1,
                'name': 'max'
            },
            {
                'id': 2,
                'name': 'giuseppe'
            },
            {
                'id': 3,
                'name': 'chatal'
            }
        ],
        'public_key': public_key_1,
        'private_key': private_key_1,
    }

    public_key_2, private_key_2 = generate_paillier_keypair(key_size=256)

    election_2 = {
        'id': 2,
        'candidates': [
            {
                'id': 1,
                'name': 'trump'
            },
            {
                'id': 2,
                'name': 'giorgia'
            },

        ],
        'public_key': public_key_2,
        'private_key': private_key_2,
    }

    blockchain.new_vote(1, encrypt(2, public_key_1), encrypt(5, public_key_1))
    blockchain.new_vote(2, encrypt(2, public_key_2), encrypt(1, public_key_2))
    blockchain.new_vote(2, encrypt(1, public_key_2), encrypt(1, public_key_2))
    blockchain.new_vote(1, encrypt(2, public_key_1), encrypt(3, public_key_1))

    pof1 = blockchain.proof_of_work(blockchain.last_block.proof)
    blockchain.new_block(pof1)

    blockchain.new_vote(1, encrypt(2, public_key_1), encrypt(1, public_key_1))
    blockchain.new_vote(1, encrypt(3, public_key_1), encrypt(3, public_key_1))
    blockchain.new_vote(2, encrypt(1, public_key_2), encrypt(6, public_key_2))
    blockchain.new_vote(1, encrypt(1, public_key_1), encrypt(3, public_key_1))

    pof1 = blockchain.proof_of_work(blockchain.last_block.proof)
    blockchain.new_block(pof1)

    tally_votes_1 = blockchain.vote_counter(election_1['id'], election_1['public_key'], election_1['private_key'])
    # (1, max) get 3 = 3
    # (2, giuseppe) get 3 + 1 + 5 = 9
    # (3, chatal) get 3 = 3
    assert tally_votes_1[1] == 3
    assert tally_votes_1[2] == 9
    assert tally_votes_1[3] == 3   


    tally_votes_2 = blockchain.vote_counter(election_2['id'], election_2['public_key'], election_2['private_key'])
    # (1, trump) 1 + 6 = 7
    # (2, giorgia) 1 = 1 
    assert tally_votes_2[1] == 7
    assert tally_votes_2[2] == 1





