from pydantic import BaseModel
from sqlmodel import Field, SQLModel

class TripDB(SQLModel, table=True):
    id: int | None = Field(default=None,primary_key=True)
    name: str
    destination: str 
    duration: int 
    price: float
    group_size: int 


class Trip(BaseModel):
    name: str
    destination: str
    duration: int
    price: float
    group_size: int

class TripOut(Trip):
    id: int
