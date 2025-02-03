import json
import hashlib
from block import Block
from vote import Vote
from typing import List
import time
from encryption.paillier import decrypt, encrypted_addition, encrypt


class Chain:
    def __init__(self):
        self.blocks: List[Block] = []
        self.current_votes: List[Vote] = []

        # set Pow difficulty
        self.POW_DIFFICULTY = 4

        # create the genesis block
        self.new_block(previous_hash="1", proof=10)

    @property
    def last_block(self) -> Block:
        """return the last block object in the chain"""
        return self.blocks[-1]

    @staticmethod
    def hash(block: Block) -> str:
        """Creates a SHA-256 hash of a Block"""
        block_string = json.dumps(block.as_dict(), sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def new_block(self, proof: int, previous_hash: str | None = None) -> Block:
        """Create a new block and add it in the chain"""

        if not previous_hash:
            previous_hash = self.hash(self.blocks[-1])

        block = Block(
            index=len(self.blocks) + 1,
            timestamp=time.time(),
            votes=self.current_votes,
            proof=proof,
            previous_hash=previous_hash,
        )

        self.current_votes = []
        self.blocks.append(block)

        return block

    def new_vote(
        self, election_id: int, encrypted_candidate_id: int, encrypted_votes: int 
    ) -> int:
        """create a new vote to go into then next mined block, return the idx of the block that will hold this vote"""

        new = Vote(election_id, encrypted_candidate_id, encrypted_votes)
        self.current_votes.append(new)

        return self.last_block.index + 1

    def proof_of_work(self, last_proof: int) -> int:
        """Pow algo: find a number p such that hash(pp') contains 4 leading 0s (where p is the previous pow, p' is the new)"""

        new_proof = 0
        while not self.is_valid_pow(last_proof, new_proof):
            new_proof += 1

        return new_proof

    def is_valid_pow(self, last_pow: int, new_pow: int) -> bool:
        guess = f"{last_pow}{new_pow}".encode()
        hashed_guess = hashlib.sha256(guess).hexdigest()
        return hashed_guess[: self.POW_DIFFICULTY] == "0" * self.POW_DIFFICULTY

    def vote_counter(self, election_id: int, public_key, private_key) -> dict:
        """ return a dict where keys are candidate_id and value the number of votes that they got in the election_id as param """
        ZERO = encrypt(0, public_key)
        result = {}
        for block in self.blocks:
            for vote in block.votes:
                if vote.election_id == election_id:
                    candidate_id = decrypt(vote.encrypted_candidate_id, private_key)

                    result[candidate_id] = encrypted_addition(
                        result.get(candidate_id, ZERO),
                        vote.encrypted_votes,
                        public_key
                    )

        for key in result:
            result[key] = decrypt(result[key], private_key)

        return result
