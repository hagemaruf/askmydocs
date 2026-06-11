import ollama


def generate_answer(question: str, context: str):

    prompt = f"""
You are an AI assistant.

Answer the user's question ONLY based on the provided context.

Context:
{context}

Question:
{question}
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

    answer = response["message"]["content"]

    return answer