
import fitz
from fastapi.testclient import TestClient
from app.main import app

# Create a test client for our FastAPI application
client = TestClient(app)


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


def test_valid_pdf_upload():
    # Create a sample PDF in memory
    document = fitz.open()
    page = document.new_page()

    page.insert_text(
        (72, 72),
        "Machine learning is a subset of artificial intelligence."
    )

    pdf_bytes = document.tobytes()
    document.close()

    # Upload the PDF to our API
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

    # Check the response
    assert response.status_code == 200

    data = response.json()

    assert data["filename"] == "sample.pdf"
    assert data["total_pages"] == 1
    assert data["pages"][0]["page_number"] == 1
    assert "Machine learning" in data["pages"][0]["text"]
