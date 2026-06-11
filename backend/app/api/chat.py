from fastapi import APIRouter
from pydantic import BaseModel

from app.rag.embedding_service import create_embedding
from app.rag.chroma_service import search_similar

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


@router.post("/chat")
async def chat(request: ChatRequest):

    # Create embedding from question
    query_embedding = create_embedding(request.question)

    # Search similar chunks
    results = search_similar(query_embedding)

    documents = results["documents"][0]

    return {
        "question": request.question,
        "relevant_chunks": documents
    }