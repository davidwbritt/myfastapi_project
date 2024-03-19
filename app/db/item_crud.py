from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pymongo

from db.models import Item

# MongoDB connection (update "mydatabase" to your db name)
mongo_ip="172.17.0.3"
mongo_port="27017"
client = pymongo.MongoClient("mongodb://"+mongo_ip+":"+mongo_port+"/")
database_name="mydatabase"

db = client[database_name]
app = FastAPI()

def getApp():
    return app

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