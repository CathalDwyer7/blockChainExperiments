import hashlib
from .vote import Vote
from typing import List
from dataclasses import dataclass, asdict

@dataclass
class Block:
    index: int
    timestamp: float
    votes: List[Vote] 
    proof: int
    previous_hash: str

    def as_dict(self):
        result = asdict(self)
        result ["votes"] = [vote.as_dict() for vote in self.votes]
        return result
    
