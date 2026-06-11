from sentence_transformers import SentenceTransformer

# Load model sekali saat startup
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embedding(text: str):

    embedding = model.encode(text)

    return embedding.tolist()