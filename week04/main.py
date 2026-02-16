from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select
from database import engine, init_db
from models import Trip, TripDB, TripOut

init_db()
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

