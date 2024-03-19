from fastapi import FastAPI, HTTPException
from db.item_crud import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)