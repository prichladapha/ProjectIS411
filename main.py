from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    pname: str
    price: float | None = None
    description: str
    categoryID: int
    uid: int
    tags: list[str] = []

class ItemOut(Item):
    id: int

app = FastAPI()

item_db = []

@app.get("/items/")
async def read_items() -> list[ItemOut]:
    return item_db

@app.get("/items/{item_id}", response_model=ItemOut) 
async def read_item(item_id: int):  
    for item in item_db:
        if item["id"] == item_id:  
            return item

@app.post("/items/")
async def create_item(item: Item)-> ItemOut:
    new_item = {
        "id": len(item_db) + 1,
        **item.model_dump(),
    }
    item_db.append(new_item)
    return new_item

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item) -> ItemOut:
    new_item = {
        "id": item_id,
        **item.model_dump()
    }

    for i in range(len(item_db)):
        if item_db[i]["id"] == item_id:
            item_db[i] = new_item
            break
    return new_item