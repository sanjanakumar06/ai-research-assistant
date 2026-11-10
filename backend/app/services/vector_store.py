
from pathlib import Path

import chromadb

from app.services.embeddings import generate_embeddings


# Store the database inside the backend folder
DB_PATH = Path(__file__).resolve().parents[2] / "chroma_db"

client = chromadb.PersistentClient(path=str(DB_PATH))

collection = client.get_or_create_collection(
    name="research_documents",
    embedding_function=None
)


def store_chunks(chunks: list[dict], document_id: str):
    """
    Generate embeddings and store chunks in ChromaDB.
    """

    if not chunks:
        return

    texts = [chunk["text"] for chunk in chunks]

    embeddings = generate_embeddings(texts)

    ids = [
        f"{document_id}_chunk_{index}"
        for index in range(len(chunks))
    ]

    metadata = [
        {
            "document_id": document_id,
            "filename": chunk["filename"],
            "page_number": chunk["page_number"],
            "chunk_index": chunk["chunk_index"]
        }
        for chunk in chunks
    ]

    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadata
    )


def search_chunks(query: str, top_k: int = 5):
    """
    Retrieve the most semantically similar chunks.
    """

    if top_k < 1:
        raise ValueError("top_k must be positive")

    if collection.count() == 0:
        return {
            "ids": [[]],
            "documents": [[]],
            "metadatas": [[]],
            "distances": [[]]
        }

    query_embedding = generate_embeddings([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"]
    )

    return results
