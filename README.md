# Enterprise Knowledge Assistant

An internal AI-powered knowledge assistant built using a Retrieval-Augmented Generation (RAG) architecture.

## Features

- Document ingestion (Markdown)
- Text chunking with overlap
- Semantic search using vector embeddings
- Local embedding model (nomic-embed-text via Ollama)
- Local LLM-based answer generation (llama3 via Ollama)
- Grounded responses with source attribution
- Hallucination control ("I don't know" fallback)

## Tech Stack

- FastAPI (backend API)
- Chroma (vector database)
- Ollama (local LLM runtime)
  - llama3 for generation
  - nomic-embed-text for embeddings

## Architecture

Documents → Chunking → Embedding → Vector Store → Retrieval → LLM → Answer + Sources

## Example

**Question:**
What technologies are used?

**Answer:**
- FastAPI
- Chroma vector database
- nomic-embed-text for embeddings
- Ollama (llama3) for generation

**Sources:**
- architecture.md

## Goal

Enable employees to query internal knowledge and receive accurate, source-grounded answers without relying on external APIs.

## Notes

- Fully local (no external API dependencies)
- Designed for extensibility (future: chat memory, reranking, multi-source retrieval)

## Roadmap

- [ ] Dynamic retrieval (adaptive top_k)
- [ ] Reranking
- [ ] Chat memory
- [ ] Multi-document filtering
