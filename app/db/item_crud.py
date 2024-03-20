
from pydantic import BaseModel
from db.models import Item
from core.config import *
from core.config import app


@app.get("/")

async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    item = db.items.find_one({"_id": item_id})
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items/")
async def create_item(item: Item):
    db.items.insert_one(item.model_dump())
    return item