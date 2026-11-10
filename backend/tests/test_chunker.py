
import pytest

from app.services.chunker import chunk_text, chunk_document


def test_short_text():
    text = "Hello world"

    chunks = chunk_text(text, chunk_size=100, overlap=20)

    assert chunks == ["Hello world"]


def test_overlapping_chunks():
    text = "ABCDEFGHIJ"

    chunks = chunk_text(text, chunk_size=5, overlap=2)

    assert chunks == [
        "ABCDE",
        "DEFGH",
        "GHIJ"
    ]


def test_empty_text():
    assert chunk_text("") == []


def test_invalid_overlap():
    with pytest.raises(ValueError):
        chunk_text("Hello", chunk_size=5, overlap=5)


def test_document_metadata():
    pages = [
        {
            "page_number": 1,
            "text": "Machine learning is useful."
        },
        {
            "page_number": 2,
            "text": "Neural networks learn patterns."
        }
    ]

    chunks = chunk_document(
        pages,
        filename="research.pdf",
        chunk_size=100,
        overlap=20
    )

    assert len(chunks) == 2
    assert chunks[0]["filename"] == "research.pdf"
    assert chunks[0]["page_number"] == 1
    assert chunks[1]["page_number"] == 2
    assert chunks[0]["chunk_index"] == 0
