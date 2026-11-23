
import pytest

from app.services import rag


@pytest.fixture
def mock_search_results():
    return {
        "documents": [[
            "Gradient descent is used to minimize loss."
        ]],
        "metadatas": [[{
            "document_id": "test_document",
            "filename": "machine_learning.pdf",
            "page_number": 2,
            "chunk_index": 0
        }]],
        "distances": [[0.19]]
    }


def test_answer_question(monkeypatch, mock_search_results):

    monkeypatch.setattr(
        rag,
        "search_chunks",
        lambda *args, **kwargs: mock_search_results
    )

    monkeypatch.setattr(
        rag,
        "generate_answer",
        lambda *args: "Gradient descent minimizes loss. [1]"
    )

    result = rag.answer_question(
        "What is gradient descent used for?"
    )

    assert "minimizes loss" in result["answer"]
    assert len(result["sources"]) == 1
    assert result["sources"][0]["filename"] == "machine_learning.pdf"
    assert result["sources"][0]["page_number"] == 2
    assert result["sources"][0]["cited"] is True


def test_invalid_citation(monkeypatch, mock_search_results):

    monkeypatch.setattr(
        rag,
        "search_chunks",
        lambda *args, **kwargs: mock_search_results
    )

    monkeypatch.setattr(
        rag,
        "generate_answer",
        lambda *args: "Gradient descent minimizes loss. [99]"
    )

    result = rag.answer_question("What is gradient descent?")

    assert "[99]" not in result["answer"]
    assert result["sources"][0]["cited"] is False


def test_empty_database(monkeypatch):

    monkeypatch.setattr(
        rag,
        "search_chunks",
        lambda *args, **kwargs: {
            "documents": [[]],
            "metadatas": [[]],
            "distances": [[]]
        }
    )

    result = rag.answer_question("What is machine learning?")

    assert result["answer"] == "No relevant documents found."
    assert result["sources"] == []


def test_empty_question():

    with pytest.raises(ValueError):
        rag.answer_question("   ")


def test_uncited_source(monkeypatch, mock_search_results):

    monkeypatch.setattr(
        rag,
        "search_chunks",
        lambda *args, **kwargs: mock_search_results
    )

    monkeypatch.setattr(
        rag,
        "generate_answer",
        lambda *args: "Gradient descent minimizes loss."
    )

    result = rag.answer_question("What is gradient descent?")

    assert result["sources"][0]["cited"] is False
