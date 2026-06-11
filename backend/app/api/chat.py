from fastapi import APIRouter
from pydantic import BaseModel

from app.rag.embedding_service import create_embedding
from app.rag.chroma_service import search_similar
from app.services.llm_service import generate_answer

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


@router.post("/chat")
async def chat(request: ChatRequest):

    # Create embedding from question
    query_embedding = create_embedding(request.question)

    # Search relevant chunks
    results = search_similar(query_embedding)

    documents = results["documents"][0]

    # Combine chunks into context
    context = "\n\n".join(documents)

    # Generate AI answer
    answer = generate_answer(
        question=request.question,
        context=context
    )

    return {
        "question": request.question,
        "answer": answer,
        "context_used": documents
    }