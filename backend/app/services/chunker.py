
def chunk_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 200
) -> list[str]:
    """
    Split text into overlapping chunks.

    Args:
        text: Text to split.
        chunk_size: Maximum characters per chunk.
        overlap: Characters shared between chunks.

    Returns:
        List of text chunks.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be nonnegative and smaller than chunk_size"
        )

    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))

        chunk = text[start:end]
        chunks.append(chunk)

        if end == len(text):
            break

        start = end - overlap

    return chunks


def chunk_document(
    pages: list[dict],
    filename: str,
    chunk_size: int = 1000,
    overlap: int = 200
) -> list[dict]:
    """
    Chunk a PDF document while preserving source metadata.
    """

    all_chunks = []

    for page in pages:
        text_chunks = chunk_text(
            page["text"],
            chunk_size=chunk_size,
            overlap=overlap
        )

        for chunk_index, text in enumerate(text_chunks):
            all_chunks.append({
                "filename": filename,
                "page_number": page["page_number"],
                "chunk_index": chunk_index,
                "text": text
            })

    return all_chunks
