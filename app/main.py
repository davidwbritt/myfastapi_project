from fastapi import FastAPI, HTTPException
from db.item_crud import getApp

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(getApp(), host="0.0.0.0", port=5000)