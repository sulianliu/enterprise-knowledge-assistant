# AGENTS.md

## Project Overview
This is a backend-only RAG (Retrieval-Augmented Generation) system.

Goal:
Answer user questions based on internal documents with source attribution.

---

## Tech Stack
- Python
- FastAPI
- Chroma (vector database)

---

## Project Structure
- backend/: main application
- backend/rag/: RAG pipeline (ingest, chunking, embedding, retrieval)
- data/docs/: source documents

---

## Rules for Code Generation

- Keep implementation simple and readable
- Do NOT introduce unnecessary frameworks (no LangChain, no GraphRAG)
- Use plain Python + FastAPI
- Keep functions small and modular
- Preserve metadata (source, chunk_id) throughout pipeline

---

## RAG Design Constraints

- Chunk size: ~300–500
- Use overlap for chunking
- Always return sources with answers
- If answer not found in context → return "I don't know"

---

## API Design

POST /query
- input: { "question": string }
- output: { "answer": string, "sources": string[] }

---

## Non-Goals (Important)

Do NOT implement:
- frontend
- authentication
- multi-user system
- agent workflows

Focus ONLY on core RAG pipeline.

---

## Development Style

- Prefer clarity over abstraction
- Avoid over-engineering
- Keep MVP scope tight
