from fastapi import FastAPI
from app.core.routers import query_router

app = FastAPI()

app.include_router(query_router)

@app.get("/")
async def root():
    return {"message": "Welcome to ChatGPT-like API"}
