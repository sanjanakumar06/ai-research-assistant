# AI Research Assistant

A full-stack AI research assistant that will use Retrieval-Augmented Generation (RAG) to answer questions about uploaded PDF documents with source citations.

## Project Overview

The application is being developed to allow users to upload PDFs, search their contents, and ask natural-language questions grounded in the uploaded documents.

## Tech Stack

- **Backend:** Python, FastAPI
- **PDF Processing:** PyMuPDF
- **Frontend (planned):** React, TypeScript
- **LLM (planned):** OpenAI API
- **Vector Database (planned):** ChromaDB
- **Testing:** pytest

## Current Features

- PDF upload through a REST API
- Text extraction with page-level metadata
- File validation and upload size limits
- Automated API tests
- Interactive API documentation using Swagger UI

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/sanjanakumar06/ai-research-assistant.git
cd ai-research-assistant/backend
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the backend

```bash
python -m uvicorn app.main:app --reload --port 8001
```

Open `http://127.0.0.1:8001/docs` to test the API.

### 5. Run tests

```bash
python -m pytest -v
```

## Roadmap

- [x] FastAPI backend setup
- [x] PDF upload and text extraction
- [x] Automated API tests
- [ ] Text chunking and embeddings
- [ ] Vector similarity search using ChromaDB
- [ ] LLM-generated answers with source citations
- [ ] React frontend
- [ ] Deployment

## Project Status

In active development.