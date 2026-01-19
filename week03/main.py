from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None  
    tags: list[str] = []

class ItemOut(Item):
    id: int

app = FastAPI()

item_db = []

@app.get("/items/")
async def raed_items() -> list[ItemOut]:
    return item_db

@app.post("/items/")
async def create_item(item: Item)-> ItemOut:
    new_item = {
        "id": len(item_db) + 1,
        **item.model_dump(),
        "tax": item.price * .07
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
