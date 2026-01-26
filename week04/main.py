from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select

class TripDB(SQLModel, table=True):
    id: int | None = Field(default=None,primary_key=True)
    name: str
    destination: str 
    duration: int 
    price: float
    group_size: int 

engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)

class Trip(BaseModel):
    name: str
    destination: str
    duration: int
    price: float
    group_size: int

class TripOut(Trip):
    id: int

app = FastAPI() 

@app.get("/trips/{trip_id}")
async def read_trip(trip_id: int) -> TripOut:
    with Session(engine) as session:
        statement = select(TripDB).where(TripDB.id == trip_id)
        trip = session.exec(statement).first()

        if trip != None:
            print(trip)
            return trip
    raise HTTPException(
        status_code=404,
        detail="Trip not found"
    )
    
def insert_trip():
    trip_1 =TripDB(name='Sit still', destination='Home', duration=3, price=500.00, group_size=1)
    trip_2 =TripDB(name='Sing a song', destination='School', duration=5, price=10000.00, group_size=4)
    trip_3 =TripDB(name='watch concert', destination='Impact arena', duration=3, price=7500.00, group_size=7)

    with Session(engine) as s:
        s.add(trip_1)
        s.add(trip_2)
        s.add(trip_3)
        s.commit()

