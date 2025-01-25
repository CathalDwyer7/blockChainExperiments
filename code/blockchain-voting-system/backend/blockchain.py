import hashlib
import json
import time
from encryption.paillier import encrypt, decrypt, generate_paillier_keypair
from encryption.blind_signature import blind_message, sign_blinded_message, unblind_signature, generate_rsa_keypair


class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.create_block(previous_hash="1")  # Genesis block

        # Generate encryption keys
        self.public_key, self.private_key = generate_paillier_keypair()
        self.blind_public_key, self.blind_private_key = generate_rsa_keypair()

    def create_block(self, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            "timestamp": time.time(),
            'transactions': self.current_transactions,
            'previous_hash': previous_hash,
            "hash": None,
        }
        block["hash"] = self.hash(block)
        self.current_transactions = []
        self.chain.append(block)
        return block

    def add_transaction(self, voter_id, election_id, votes, proposal):
        # Encrypt vote
        encrypted_vote = encrypt(votes, self.public_key)

        # Create blinded vote
        blinded_vote, blinding_factor = blind_message(
            encrypted_vote, self.blind_public_key)

        # Sign blinded vote
        signed_blinded_vote = sign_blinded_message(
            blinded_vote, self.blind_private_key)

        # Unblind the vote signature
        unblinded_signature = unblind_signature(
            signed_blinded_vote, blinding_factor, self.blind_public_key)

        self.current_transactions.append({
            'voter_id': voter_id,
            'election_id': election_id,
            "proposal": proposal,
            'votes': votes,
            'quadratic_cost': votes ** 2,
            'encrypted_vote': encrypted_vote,
            'signature': unblinded_signature,
        })

    def tally_votes(self, election_id):
        """Tally votes for a specific election."""
        vote_counts = {}
        for block in self.chain:
            for transaction in block["transactions"]:
                print(f"Processing Transaction: {transaction}")  # Debugging
                if transaction["election_id"] == election_id:
                    proposal = transaction["proposal"]
                    encrypted_vote = int(transaction["encrypted_vote"])

                    print(f"Encrypted Vote: {encrypted_vote}, Type: {type(encrypted_vote)}")
                    
                    # Decrypt the vote
                    decrypted_vote = decrypt(encrypted_vote, self.private_key)
                    vote_counts[proposal] = vote_counts.get(
                        proposal, 0) + decrypted_vote
        return vote_counts

    @staticmethod
    def hash(block):
        """Generate a SHA-256 hash of a block."""
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def is_valid_chain(self):
        """Check if the blockchain is valid."""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # Validate hash
            if current["previous_hash"] != previous["hash"]:
                return False

            # Recalculate hash and compare
            if current["hash"] != self.hash(current):
                return False

        return True