from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Text, Boolean, ForeignKey
from extensions import db
import enum

class ElectionStatus(enum.Enum):
    UPCOMING = 'upcoming'
    ONGOING = 'ongoing'
    COMPLETED ='completed'

class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullabe=False)
    is_admin: Mapped[Boolean] = mapped_column(Boolean, default=False) 

class Election(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    start_credits: Mapped[int] = mapped_column(Integer, nullable=False)
    start_date: Mapped[int] = mapped_column(Integer, nullable=False) 
    end_date: Mapped[int] = mapped_column(Integer, nullable=False) 
    description: Mapped[str] = mapped_column(Text, nullable=True)

    @property
    def status(self) -> ElectionStatus:
        """ Evaluate current status dinamimcally """
        now = int(datetime.utcnow().timestamp())

        if now < self.start_date:
            return ElectionStatus.UPCOMING
        elif self.start_date <= now <= self.end_date:
            return ElectionStatus.ONGOING
        else:
            return ElectionStatus.COMPLETED
        
class ElectionCredits(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    election_id: Mapped[int] = mapped_column(Integer, ForeignKey('election.id'), nullable=False)
    credits_left: Mapped[int] = mapped_column(Integer, nullable=False)

class Candidates(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    election_id: Mapped[int] = mapped_column(Integer, ForeignKey('election.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
