from dataclasses import dataclass, asdict

@dataclass
class Vote:
    election_id: int
    encrypted_candidate_id: int
    encrypted_votes: int 
    
    def as_dict(self) -> dict:
        """ create a dict rappresenation of the object """
        return asdict(self)
