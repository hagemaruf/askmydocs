from fastapi import APIRouter
from pydantic import BaseModel
from ollama import Client
from app.config import OLLAMA_HOST

client = Client(host=OLLAMA_HOST)

router = APIRouter()

class TitleRequest(BaseModel):
    question: str

@router.post("/generate-title")
async def generate_title(
    request: TitleRequest
):
    prompt = f"""
Generate a very short title
(3-5 words only)
for this conversation.

Question:
{request.question}

Rules:
- no quotes
- no punctuation
- concise
- professional
"""

    response = client.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    title = response["message"]["content"]

    return {
        "title": title.strip()
    }