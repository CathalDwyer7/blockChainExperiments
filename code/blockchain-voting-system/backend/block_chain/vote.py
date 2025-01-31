from dataclasses import dataclass, asdict

@dataclass
class Vote:
    user_id: str
    election_id: str
    candidate_id: str
    votes: int
     
    def as_dict(self) -> dict:
        """ create a dict rappresenation of the object """
        return asdict(self)
