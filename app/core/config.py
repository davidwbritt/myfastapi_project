import pymongo
from fastapi import FastAPI, HTTPException
from pymongo.collection import ReturnDocument

# MongoDB connection (update "mydatabase" to your db name)
mongo_ip="172.17.0.3"
mongo_port="27017"
client = pymongo.MongoClient("mongodb://"+mongo_ip+":"+mongo_port+"/")
database_name="mydatabase"


db = client[database_name]
app = FastAPI()

# def getApp():
#     return app