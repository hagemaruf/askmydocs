from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.rag.embedding_service import create_embedding
from app.rag.chroma_service import search_similar
from app.services.llm_service import stream_answer

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


@router.post("/chat")
async def chat(request: ChatRequest):

    query_embedding = create_embedding(
        request.question
    )

    results = search_similar(query_embedding)

    documents = results["documents"][0]

    context = "\n\n".join(documents)

    generator = stream_answer(
        question=request.question,
        context=context
    )

    return StreamingResponse(
        generator,
        media_type="text/plain"
    )