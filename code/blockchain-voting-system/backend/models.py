from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Text, Boolean, ForeignKey, JSON
from extensions import db
import enum
from dataclasses import dataclass
from block_chain.encryption.paillier import generate_paillier_keypair

class ElectionStatus(enum.Enum):
    """Enumeration representing the possible statuses of an election."""
    UPCOMING = 'upcoming'
    ONGOING = 'ongoing'
    COMPLETED ='completed'

@dataclass
class User(db.Model):
    """
    Represents a user in the system.

    Attributes:
        `id` (`int`): Unique identifier for the user.
        `username` (`str`): The username of the user (unique).
        `password` (`str`): The hashed password of the user.
        `is_admin` (`bool`): Indicates whether the user has administrative privileges.
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False) 

    #public_key: Mapped[dict] = mapped_column(JSON, nullable=True) 


@dataclass
class Election(db.Model):
    """
    Represents an election in the system.

    Attributes:
        `id` (`int`): Unique identifier for the election.
        `title` (`str`): The title of the election.
        `start_credits` (`int`): The initial credits assigned to each voter.
        `start_date` (`int`): The UNIX timestamp representing the start time of the election.
        `end_date` (`int`): The UNIX timestamp representing the end time of the election.
        `description` (`str`, optional): A textual description of the election.
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    start_credits: Mapped[int] = mapped_column(Integer, nullable=False)
    start_date: Mapped[int] = mapped_column(Integer, nullable=False) 
    end_date: Mapped[int] = mapped_column(Integer, nullable=False) 
    description: Mapped[str] = mapped_column(Text, nullable=True)

    public_key: Mapped[dict] = mapped_column(JSON, nullable=True) 
    private_key: Mapped[dict] = mapped_column(JSON, nullable=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs) #call the init form dataclasses

        if not self.public_key or not self.private_key:
            (n, g), (lam, mu, p) = generate_paillier_keypair()
            self.public_key = {'n': n, 'g': g}
            self.private_key = {'lambda': lam, 'mu': mu, 'p': p}

    @property
    def status(self) -> ElectionStatus:
        """
        Determines the current status of the election dynamically.

        Returns:
            `ElectionStatus`: The current status of the election (`UPCOMING`, `ONGOING`, `COMPLETED`).
        """
        now = int(datetime.utcnow().timestamp())
        if now < self.start_date:
            return ElectionStatus.UPCOMING
        elif self.start_date <= now <= self.end_date:
            return ElectionStatus.ONGOING
        else:
            return ElectionStatus.COMPLETED
        

@dataclass
class ElectionCredits(db.Model):
    """
    Represents the credit system for quadratic voting in an election.

    Attributes:
        `id` (`int`): Unique identifier for the credit record.
        `user_id` (`int`): Foreign key referencing the user participating in the election.
        `election_id` (`int`): Foreign key referencing the election.
        `credits_left` (`int`): The number of credits remaining encrypted with the public_key of the election.
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    election_id: Mapped[int] = mapped_column(Integer, ForeignKey('election.id'), nullable=False)
    credits_left: Mapped[int] = mapped_column(Integer, nullable=False)


@dataclass
class Candidates(db.Model):
    """
    Represents a candidate participating in an election.

    Attributes:
        `id` (`int`): Unique identifier for the candidate.
        `election_id` (`int`): Foreign key referencing the associated election.
        `name` (`str`): The name of the candidate.
        `description` (`str`, optional): Additional information or manifesto of the candidate.
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    election_id: Mapped[int] = mapped_column(Integer, ForeignKey('election.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
