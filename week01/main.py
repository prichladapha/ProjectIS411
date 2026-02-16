from typing import Union
from fastapi import FastAPI

app = FastAPI()

fake_items_db = [
    {"item_name": "11111"},
    {"item_name": "22222"},
    {"item_name": "33333"},
    {"item_name": "44444"},
    {"item_name": "55555"},
    {"item_name": "66666"},
    {"item_name": "77777"},
    {"item_name": "88888"},
    {"item_name": "99999"},
    {"item_name": "aaaaa"},
]

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10) :
    return fake_items_db[skip : skip + limit]