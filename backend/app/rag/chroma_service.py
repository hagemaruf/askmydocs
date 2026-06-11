import chromadb

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="documents"
)


def add_document(chunk: str, embedding, source: str):

    collection.add(
        documents=[chunk],
        embeddings=[embedding],
        metadatas=[{"source": source}],
        ids=[f"{source}_{hash(chunk)}"]
    )


def search_similar(query_embedding, top_k=3):

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results