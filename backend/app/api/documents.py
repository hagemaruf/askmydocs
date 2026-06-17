from fastapi import APIRouter
from app.rag.chroma_service import collection

router = APIRouter()


@router.get("/documents")
def get_documents():

    result = collection.get()

    metadata_list = result.get("metadatas", [])

    documents = {}

    for metadata in metadata_list:

        document_id = metadata.get("document_id")

        if not document_id:
            continue

        if document_id not in documents:

            documents[document_id] = {
                "document_id": document_id,
                "filename": metadata.get("source"),
                "uploaded_at": metadata.get("uploaded_at"),
                "chunks": 0
            }

        documents[document_id]["chunks"] += 1

    return list(documents.values())

@router.delete("/documents/{document_id}")
def delete_document(document_id: str):

    result = collection.get()

    ids_to_delete = []
    metadata_list = result.get("metadatas", [])
    ids = result.get("ids", [])

    for index, metadata in enumerate(metadata_list):

        if metadata.get("document_id") == document_id:
            ids_to_delete.append(ids[index])

    if ids_to_delete:
        collection.delete(ids=ids_to_delete)

    return {
        "message": "Document deleted"
    }

@router.get("/documents/{document_id}/chunks")
def get_document_chunks(document_id: str):

    result = collection.get(
        include=["documents", "metadatas"]
    )

    chunks = []

    documents = result.get("documents", [])
    metadatas = result.get("metadatas", [])

    for doc, metadata in zip(documents, metadatas):

        if metadata.get("document_id") == document_id:

            chunks.append({
                "page": metadata.get("page"),
                "chunk": metadata.get("chunk"),
                "content": doc
            })

    chunks.sort(
        key=lambda x: (
            x["page"],
            x["chunk"]
        )
    )

    return chunks