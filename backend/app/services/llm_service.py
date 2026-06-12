import ollama


def stream_answer(
    question: str,
    context: str,
    sources: list,
    history: list
):

    messages = []

    system_prompt = f"""
You are an AI assistant.

Answer ONLY using the provided context.

Context:
{context}
"""

    messages.append({
        "role": "system",
        "content": system_prompt
    })

    # Add conversation history
    for message in history:

        messages.append({
            "role": message.role,
            "content": message.content
        })

    # Add current question
    messages.append({
        "role": "user",
        "content": question
    })

    stream = ollama.chat(
        model="llama3.2",
        messages=messages,
        stream=True
    )

    for chunk in stream:

        content = chunk["message"]["content"]

        yield content

    yield "\n\nSources:\n"

    for source in sources:

        yield f"- {source['source']} (page {source['page']})\n"