from pydantic import BaseModel
from .models import Item, User
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

@app.post("/items/{custom_id}")
async def create_or_update_item(custom_id: str, item: Item):
    # Attempt to update the item if it exists
    updated_item = db.items.find_one_and_update(
        {"custom_id": custom_id},
        {"$set": item.model_dump(exclude_unset=True)},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )

    # If the item was updated or inserted, return it
    if updated_item:
        return Item(**updated_item)
    else:
        # This branch might not be reached due to upsert=True, but it's good practice to handle potential errors
        raise HTTPException(status_code=500, detail="The item could not be updated or created")


def getApp():
    return app


from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pymongo import MongoClient
from passlib.context import CryptContext

security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post("/users/")
async def create_user(user: User):
    db.users.insert_one(user.model_dump())
    return user

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = db.users.find_one({"username": credentials.username})
    if user and pwd_context.verify(credentials.password, user['password']):
        return credentials.username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Basic"},
    )
