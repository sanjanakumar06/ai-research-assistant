
from fastapi.testclient import TestClient

from app.main import app
from app.routes import questions


client = TestClient(app)


def test_ask_question(monkeypatch):

    def mock_answer(question, top_k):
        return {
            "question": question,
            "answer": "Gradient descent minimizes loss. [1]",
            "sources": [{
                "source_id": 1,
                "filename": "machine_learning.pdf",
                "page_number": 2,
                "cited": True
            }]
        }

    monkeypatch.setattr(
        questions,
        "answer_question",
        mock_answer
    )

    response = client.post(
        "/ask",
        json={
            "question": "What is gradient descent?",
            "top_k": 3
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "minimizes loss" in data["answer"]
    assert len(data["sources"]) == 1
    assert data["sources"][0]["cited"] is True


def test_empty_question():

    response = client.post(
        "/ask",
        json={"question": ""}
    )

    assert response.status_code == 422


def test_whitespace_question():

    response = client.post(
        "/ask",
        json={"question": "   "}
    )

    assert response.status_code == 400


def test_invalid_top_k():

    response = client.post(
        "/ask",
        json={
            "question": "What is machine learning?",
            "top_k": 0
        }
    )

    assert response.status_code == 422


def test_generation_failure(monkeypatch):

    def mock_failure(*args, **kwargs):
        raise RuntimeError("Model failure")

    monkeypatch.setattr(
        questions,
        "answer_question",
        mock_failure
    )

    response = client.post(
        "/ask",
        json={"question": "What is machine learning?"}
    )

    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to generate answer"
