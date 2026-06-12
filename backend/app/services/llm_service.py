import ollama


def stream_answer(question: str, context: str):

    prompt = f"""
You are an AI assistant.

Answer the user's question ONLY based on the provided context.

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