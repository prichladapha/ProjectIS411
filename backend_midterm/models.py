from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from database import engine, init_db

#create Region 
class Region(SQLModel, table=True):
    __tablename__ = "Regions"

    region_id: Optional[int] = Field(default=None, primary_key=True)
    name_th: str = Field(unique=True)
    total_population: int = Field(default=0)


class RegionCreate(SQLModel):
    name_th: str
    total_population: int = 0

class Constituency(SQLModel, table=True):
    __tablename__ = "Constituencies"

    const_id: Optional[int] = Field(default=None, primary_key=True)
    region_id: int = Field(foreign_key="Regions.region_id")
    const_number: int
    total_eligible_voters: int = Field(default=0)

class ConstituencyCreate(SQLModel):
    region_id: int
    const_number: int
    total_eligible_voters: int = 0

class Party(SQLModel, table=True):
    __tablename__ = "Parties"

    party_id: Optional[int] = Field(default=None, primary_key=True)
    party_name: str = Field(unique=True)
    party_leader: Optional[str] = None
    party_logo_url: Optional[str] = None

class PartyCreate(SQLModel):
    party_name: str
    party_leader: Optional[str] = None
    party_logo_url: Optional[str] = None

class Candidate(SQLModel, table=True):
    __tablename__ = "Candidates"

    candidate_id: Optional[int] = Field(default=None, primary_key=True)
    const_id: int = Field(foreign_key="Constituencies.const_id")
    party_id: int = Field(foreign_key="Parties.party_id")
    candidate_number: int
    full_name: str

class CandidateCreate(SQLModel):
    const_id: int
    party_id: int
    candidate_number: int
    full_name: str

class Voter(SQLModel, table=True):
    __tablename__ = "Voters"

    voter_id: Optional[int] = Field(default=None, primary_key=True)
    citizen_id: str = Field(unique=True)
    full_name: str
    const_id: int = Field(foreign_key="Constituencies.const_id")
    has_voted_const: int = Field(default=0)
    has_voted_list: int = Field(default=0)

class VoterCreate(SQLModel):
    citizen_id: str
    full_name: str
    const_id: int

class VoterStatusUpdate(SQLModel):
    has_voted_const: Optional[int] = None
    has_voted_list: Optional[int] = None

class Ballot(SQLModel, table=True):
    __tablename__ = "Ballots"

    ballot_id: Optional[int] = Field(default=None, primary_key=True)
    const_id: int = Field(foreign_key="Constituencies.const_id")
    candidate_id: Optional[int] = Field(default=None, foreign_key="Candidates.candidate_id")
    party_id: Optional[int] = Field(default=None, foreign_key="Parties.party_id")
    vote_type: str  # 'Constituency' หรือ 'PartyList'
    voted_at: datetime = Field(default_factory=datetime.now)

class BallotCreate(SQLModel):
    const_id: int
    candidate_id: Optional[int] = None
    party_id: Optional[int] = None
    vote_type: str  # 'Constituency' หรือ 'PartyList'