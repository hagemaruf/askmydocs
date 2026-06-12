import chromadb
import uuid

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="documents"
)


def add_documents(
    chunks,
    embeddings,
    metadatas
):

    ids = [
        str(uuid.uuid4())
        for _ in chunks
    ]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )


def search_similar(query_embedding):

    return collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )