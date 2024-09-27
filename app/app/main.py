from fastapi import FastAPI
from app.app.routers import query_router

app = FastAPI()

app.include_router(query_router)

@app.get("/")
async def root():
    return {"message": "Welcome to ChatGPT-like API"}
