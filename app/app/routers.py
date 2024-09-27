from fastapi import APIRouter
from app.app.models import QueryRequest, QueryResponse
from app.app.rag import generate_answer
# from app.app.prompts import apply_prompt

query_router = APIRouter()

@query_router.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    response_text = generate_answer(request.query)
    #response_text = apply_prompt(request.query)
    return QueryResponse(response=response_text)
