
from app.services.vector_store import store_chunks, search_chunks

sample_chunks = [
    {
        "filename": "machine_learning.pdf",
        "page_number": 1,
        "chunk_index": 0,
        "text": "Neural networks learn patterns from training data."
    },
    {
        "filename": "machine_learning.pdf",
        "page_number": 2,
        "chunk_index": 0,
        "text": "Gradient descent is an optimization algorithm used to minimize loss."
    },
    {
        "filename": "machine_learning.pdf",
        "page_number": 3,
        "chunk_index": 0,
        "text": "Supervised learning uses labeled training examples."
    }
]

store_chunks(
    sample_chunks,
    document_id="test_document"
)

results = search_chunks(
    "How do neural networks learn?",
    top_k=2
)

for text, metadata, distance in zip(
    results["documents"][0],
    results["metadatas"][0],
    results["distances"][0]
):
    print("\nRetrieved passage:", text)
    print("Source:", metadata["filename"])
    print("Page:", metadata["page_number"])
    print("Distance:", distance)
