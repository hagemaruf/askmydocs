from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.rag.embedding_service import create_embedding
from app.rag.chroma_service import search_similar
from app.services.llm_service import stream_answer

router = APIRouter()


class ChatRequest(BaseModel):
    question: str
    history: list[Message] = []

class Message(BaseModel):
    role: str
    content: str

@router.post("/chat")
async def chat(request: ChatRequest):

    # Create embedding from user question
    query_embedding = create_embedding(
        request.question
    )

    # Search similar chunks
    results = search_similar(
        query_embedding
    )

    # Retrieved documents
    documents = results["documents"][0]

    # Retrieved metadata
    metadatas = results["metadatas"][0]

    # Combine chunks into context
    context = "\n\n".join(documents)

    # Build source references
    sources = []

    seen = set()

    for metadata in metadatas:

        key = (
            metadata["source"],
            metadata["page"]
        )

        if key not in seen:

            seen.add(key)

            sources.append({
                "source": metadata["source"],
                "page": metadata["page"]
            })

    # Stream AI answer
    generator = stream_answer(
        question=request.question,
        context=context,
        sources=sources,
        history=request.history
    )

    return StreamingResponse(
        generator,
        media_type="text/event-stream"
    )