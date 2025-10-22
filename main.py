from fastapi import FastAPI
from database.connection import init_db

app = FastAPI()

@app.on_event("startup")
async def start_db():
    await init_db()

@app.get("/")
async def root():
    return {"message": "E-commerce API running successfully!"}
