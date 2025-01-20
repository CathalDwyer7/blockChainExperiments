from encryption.paillier import encrypt, decrypt, generate_paillier_keypair
from encryption.blind_signature import (
    blind_message, sign_blinded_message, unblind_signature, generate_rsa_keypair
)

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Generate encryption keys
        self.public_key, self.private_key = generate_paillier_keypair()
        self.blind_public_key, self.blind_private_key = generate_rsa_keypair()

    def create_block(self, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'transactions': self.current_transactions,
            'previous_hash': previous_hash,
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def add_transaction(self, voter_id, election_id, vote):
        # Encrypt vote
        encrypted_vote = encrypt(vote, self.public_key)

        # Create blinded vote
        blinded_vote, blinding_factor = blind_message(encrypted_vote, self.blind_public_key)

        # Sign blinded vote
        signed_blinded_vote = sign_blinded_message(blinded_vote, self.blind_private_key)

        # Unblind the vote signature
        unblinded_signature = unblind_signature(signed_blinded_vote, blinding_factor, self.blind_public_key)

        self.current_transactions.append({
            'voter_id': voter_id,
            'election_id': election_id,
            'encrypted_vote': encrypted_vote,
            'signature': unblinded_signature,
        })
