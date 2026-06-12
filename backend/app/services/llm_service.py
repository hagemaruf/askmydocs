import ollama


def stream_answer(
    question: str,
    context: str,
    sources: list
):

    prompt = f"""
You are an AI assistant.

Answer ONLY based on the provided context.

Context:
{context}

Question:
{question}
"""

    stream = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        stream=True
    )

    for chunk in stream:

        content = chunk["message"]["content"]

        yield content

    yield "\n\nSources:\n"

    for source in sources:

        yield f"- {source['source']} (page {source['page']})\n"