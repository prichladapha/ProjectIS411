from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException, status
from sqlmodel import Session, select, func
from database import engine, init_db
from models import (Region, RegionCreate, Constituency, ConstituencyCreate, Party, PartyCreate, Candidate, CandidateCreate, Voter, VoterCreate, VoterStatusUpdate, Ballot, BallotCreate )

init_db()

app = FastAPI()

# สร้าง region
@app.post("/regions", status_code=status.HTTP_201_CREATED, tags=["Regions"])
async def create_region(data: RegionCreate) -> Region:
    with Session(engine) as session:
        db_region = Region(
            name_th=data.name_th,
            total_population=data.total_population
        )
        session.add(db_region)
        session.commit()
        session.refresh(db_region)
        return db_region

# get region all
@app.get("/regions", tags=["Regions"])
async def list_regions() -> list[Region]:
    with Session(engine) as session:
        return session.exec(select(Region)).all()

# สร้าง constituencies
@app.post("/constituencies", status_code=status.HTTP_201_CREATED, tags=["Constituencies"])
async def create_constituency(data: ConstituencyCreate) -> Constituency:
    with Session(engine) as session:
        if not session.get(Region, data.region_id):
            raise HTTPException(status_code=404, detail="Region not found")
        constituency = Constituency(
            region_id=data.region_id,
            const_number=data.const_number,
            total_eligible_voters=data.total_eligible_voters
        )
        session.add(constituency)
        session.commit()
        session.refresh(constituency)
        return constituency

# เพิ่มพรรคการเมือง
@app.post("/parties", status_code=status.HTTP_201_CREATED, tags=["Parties"])
async def create_party(data: PartyCreate) -> Party:
    with Session(engine) as session:
        party = Party(
            party_name=data.party_name,
            party_leader=data.party_leader,
            party_logo_url=data.party_logo_url
        )
        session.add(party)
        session.commit()
        session.refresh(party)
        return party

# ดูรายชื่อพรรคการเมืองทั้งหมด 
@app.get("/parties")
async def list_parties() -> list[Party]:
    with Session(engine) as session:
        return session.exec(select(Party)).all()

# ดูรายชื่อพรรคการเมืองจาก party_id
@app.get("/parties/{party_id}", tags=["Parties"])
async def get_party(party_id: int) -> Party:
    with Session(engine) as session:
        party = session.get(Party, party_id)
        if not party:
            raise HTTPException(status_code=404, detail="Party not found")
        return party

# เพิ่ม candidates
@app.post("/candidates", status_code=status.HTTP_201_CREATED, tags=["Candidates"])
async def create_candidate(data: CandidateCreate) -> Candidate:
    with Session(engine) as session:
        if not session.get(Constituency, data.const_id):
            raise HTTPException(status_code=404, detail="Constituency not found")
        if not session.get(Party, data.party_id):
            raise HTTPException(status_code=404, detail="Party not found")
        candidate = Candidate(
            const_id=data.const_id,
            party_id=data.party_id,
            candidate_number=data.candidate_number,
            full_name=data.full_name
        )
        session.add(candidate)
        session.commit()
        session.refresh(candidate)
        return candidate

# เรียกดู candidates ทั้งหมด
@app.get("/candidates", tags=["Candidates"])
async def list_candidates(const_id: Optional[int] = None) -> list[Candidate]:
    with Session(engine) as session:
        query = select(Candidate)
        if const_id:
            query = query.where(Candidate.const_id == const_id)
        return session.exec(query).all()

# เรียกดู candidates by canduidates_id
@app.get("/candidates/{candidate_id}", tags=["Candidates"])
async def get_candidate(candidate_id: int) -> Candidate:
    with Session(engine) as session:
        candidate = session.get(Candidate, candidate_id)
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")
        return candidate

#เพิ่ม voters ผู้มีสิทธิ์เลือกตั้ง
@app.post("/voters", status_code=status.HTTP_201_CREATED, tags=["Voters"])
async def create_voter(data: VoterCreate) -> Voter:
    with Session(engine) as session:
        if not session.get(Constituency, data.const_id):
            raise HTTPException(status_code=404, detail="Constituency not found")
        existing = session.exec(select(Voter).where(Voter.citizen_id == data.citizen_id)).first()
        if existing:
            raise HTTPException(status_code=400, detail="Voter with this citizen_id already exists")
        voter = Voter(
            citizen_id=data.citizen_id,
            full_name=data.full_name,
            const_id=data.const_id
        )
        session.add(voter)
        session.commit()
        session.refresh(voter)
        return voter

# ดูรายชื่อผู้มีสิทธิ์เลือกตั้งทั้งหมด
@app.get("/voters", tags=["Voters"])
async def list_voters(const_id: Optional[int] = None) -> list[Voter]:
    with Session(engine) as session:
        query = select(Voter)
        if const_id:
            query = query.where(Voter.const_id == const_id)
        return session.exec(query).all()

# ดูข้อมูลผู้มีสิทธิ์เลือกตั้ง by voter_id
@app.get("/voters/{voter_id}", tags=["Voters"])
async def get_voter(voter_id: int) -> Voter:
    with Session(engine) as session:
        voter = session.get(Voter, voter_id)
        if not voter:
            raise HTTPException(status_code=404, detail="Voter not found")
        return voter

# อัพเดจข้อมูลการมาใช้สิทธิ์เลือกตั้ง
@app.patch("/voters/{voter_id}/status", tags=["Voters"])
async def update_voter_status(voter_id: int, data: VoterStatusUpdate) -> Voter:
    with Session(engine) as session:
        voter = session.get(Voter, voter_id)
        if not voter:
            raise HTTPException(status_code=404, detail="Voter not found")
        if data.has_voted_const is not None:
            voter.has_voted_const = data.has_voted_const
        if data.has_voted_list is not None:
            voter.has_voted_list = data.has_voted_list
        session.add(voter)
        session.commit()
        session.refresh(voter)
        return voter

# ลงคะแนนเสียงเลือกตั้งแบบไม่ระบุตัวตน
@app.post("/ballots", status_code=status.HTTP_201_CREATED, tags=["Ballots"])
async def cast_ballot(data: BallotCreate) -> Ballot:
    with Session(engine) as session:
        if data.vote_type not in ("Constituency", "PartyList"):
            raise HTTPException(status_code=400, detail="vote_type must be 'Constituency' or 'PartyList'")
        if not session.get(Constituency, data.const_id):
            raise HTTPException(status_code=404, detail="Constituency not found")
        if data.candidate_id and not session.get(Candidate, data.candidate_id):
            raise HTTPException(status_code=404, detail="Candidate not found")
        if data.party_id and not session.get(Party, data.party_id):
            raise HTTPException(status_code=404, detail="Party not found")
        ballot = Ballot(
            const_id=data.const_id,
            candidate_id=data.candidate_id,
            party_id=data.party_id,
            vote_type=data.vote_type
        )
        session.add(ballot)
        session.commit()
        session.refresh(ballot)
        return ballot

# ดูผลการเลือกตั้งแบบสรุป
@app.get("/ballots/summary", tags=["Ballots"])
async def ballot_summary():
    with Session(engine) as session:
        rows = session.exec(
            select(
                Constituency.const_id,
                Constituency.const_number,
                Region.name_th,
                Ballot.vote_type,
                func.count(Ballot.ballot_id).label("total_votes"),
            )
            .join(Ballot, Ballot.const_id == Constituency.const_id)
            .join(Region, Region.region_id == Constituency.region_id)
            .group_by(Constituency.const_id, Ballot.vote_type)
        ).all()

        summary: dict = {}
        for row in rows:
            key = row.const_id
            if key not in summary:
                summary[key] = {
                    "const_id": row.const_id,
                    "const_number": row.const_number,
                    "region_name": row.name_th,
                    "constituency_votes": 0,
                    "partylist_votes": 0,
                }
            if row.vote_type == "Constituency":
                summary[key]["constituency_votes"] = row.total_votes
            else:
                summary[key]["partylist_votes"] = row.total_votes

        return list(summary.values())

# ผลเลือกตั้งพรรค ทั้งประเทศ
@app.get("/results/partylist", tags=["Results"])
async def results_partylist():
    with Session(engine) as session:
        rows = session.exec(
            select(
                Party.party_id,
                Party.party_name,
                func.count(Ballot.ballot_id).label("total_votes"),
            )
            .join(Ballot, Ballot.party_id == Party.party_id)
            .where(Ballot.vote_type == "PartyList")
            .group_by(Party.party_id)
            .order_by(func.count(Ballot.ballot_id).desc())
        ).all()

        return [
            {"party_id": r.party_id, "party_name": r.party_name, "total_votes": r.total_votes}
            for r in rows
        ]

# ผลเลือกตั้งพรรค แยกตามเขต
@app.get("/results/partylist/by-constituency", tags=["Results"])
async def results_partylist_by_constituency():
    with Session(engine) as session:
        rows = session.exec(
            select(
                Constituency.const_id,
                Constituency.const_number,
                Region.name_th,
                Party.party_id,
                Party.party_name,
                func.count(Ballot.ballot_id).label("total_votes"),
            )
            .join(Ballot, Ballot.const_id == Constituency.const_id)
            .join(Region, Region.region_id == Constituency.region_id)
            .join(Party, Party.party_id == Ballot.party_id)
            .where(Ballot.vote_type == "PartyList")
            .group_by(Constituency.const_id, Party.party_id)
            .order_by(Constituency.const_id, func.count(Ballot.ballot_id).desc())
        ).all()

        grouped: dict = {}
        for r in rows:
            key = r.const_id
            if key not in grouped:
                grouped[key] = {
                    "const_id": r.const_id,
                    "const_number": r.const_number,
                    "region_name": r.name_th,
                    "parties": [],
                }
            grouped[key]["parties"].append({
                "party_id": r.party_id,
                "party_name": r.party_name,
                "total_votes": r.total_votes,
            })

        return list(grouped.values())

# ผลเลือกตั้ง ส.ส.เขต ทั้งประเทศ
@app.get("/results/constituency", tags=["Results"])
async def results_constituency():
    with Session(engine) as session:
        rows = session.exec(
            select(
                Candidate.candidate_id,
                Candidate.full_name,
                Party.party_name,
                func.count(Ballot.ballot_id).label("total_votes"),
            )
            .join(Ballot, Ballot.candidate_id == Candidate.candidate_id)
            .join(Party, Party.party_id == Candidate.party_id)
            .where(Ballot.vote_type == "Constituency")
            .group_by(Candidate.candidate_id)
            .order_by(func.count(Ballot.ballot_id).desc())
        ).all()

        return [
            {
                "candidate_id": r.candidate_id,
                "full_name": r.full_name,
                "party_name": r.party_name,
                "total_votes": r.total_votes,
            }
            for r in rows
        ]

# ผลเลือกตั้ง ส.ส.เขต แยกตามเขต
@app.get("/results/constituency/by-constituency", tags=["Results"])
async def results_constituency_by_const():
    with Session(engine) as session:
        rows = session.exec(
            select(
                Constituency.const_id,
                Constituency.const_number,
                Region.name_th,
                Candidate.candidate_id,
                Candidate.full_name,
                Party.party_name,
                func.count(Ballot.ballot_id).label("total_votes"),
            )
            .join(Ballot, Ballot.const_id == Constituency.const_id)
            .join(Region, Region.region_id == Constituency.region_id)
            .join(Candidate, Candidate.candidate_id == Ballot.candidate_id)
            .join(Party, Party.party_id == Candidate.party_id)
            .where(Ballot.vote_type == "Constituency")
            .group_by(Constituency.const_id, Candidate.candidate_id)
            .order_by(Constituency.const_id, func.count(Ballot.ballot_id).desc())
        ).all()

        grouped: dict = {}
        for r in rows:
            key = r.const_id
            if key not in grouped:
                grouped[key] = {
                    "const_id": r.const_id,
                    "const_number": r.const_number,
                    "region_name": r.name_th,
                    "candidates": [],
                }
            grouped[key]["candidates"].append({
                "candidate_id": r.candidate_id,
                "full_name": r.full_name,
                "party_name": r.party_name,
                "total_votes": r.total_votes,
            })

        return list(grouped.values())
 