
from unittest.mock import patch

import fitz
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def create_sample_pdf():
    """Generate a sample PDF in memory."""
    document = fitz.open()
    page = document.new_page()

    page.insert_text(
        (72, 72),
        "Machine learning is a subset of artificial intelligence."
    )

    pdf_bytes = document.tobytes()
    document.close()

    return pdf_bytes


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_invalid_pdf_upload():
    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "invalid.pdf",
                b"this is not a PDF",
                "application/pdf"
            )
        }
    )

    assert response.status_code == 400


@patch("app.routes.documents.store_chunks")
def test_valid_pdf_upload(mock_store):
    pdf_bytes = create_sample_pdf()

    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "sample.pdf",
                pdf_bytes,
                "application/pdf"
            )
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["filename"] == "sample.pdf"
    assert data["total_pages"] == 1
    assert data["total_chunks"] >= 1
    assert "document_id" in data

    mock_store.assert_called_once()


@patch("app.routes.documents.search_chunks")
def test_semantic_search(mock_search):

    mock_search.return_value = {
        "documents": [[
            "Neural networks learn from training data."
        ]],
        "metadatas": [[
            {
                "filename": "research.pdf",
                "page_number": 2
            }
        ]],
        "distances": [[0.25]]
    }

    response = client.get(
        "/documents/search",
        params={
            "query": "How do neural networks learn?",
            "top_k": 3
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["matches"]) == 1
    assert data["matches"][0]["filename"] == "research.pdf"
    assert data["matches"][0]["page_number"] == 2

    mock_search.assert_called_once_with(
        "How do neural networks learn?",
        3
    )


def test_search_invalid_top_k():
    response = client.get(
        "/documents/search",
        params={
            "query": "machine learning",
            "top_k": 0
        }
    )

    assert response.status_code == 422
