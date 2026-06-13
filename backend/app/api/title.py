from fastapi import APIRouter
from pydantic import BaseModel
import ollama

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

    response = ollama.chat(
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