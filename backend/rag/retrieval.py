from backend.rag.chunking import chunk_documents
from backend.rag.embedding import embed_text, embed_texts
from backend.rag.ingest import load_markdown_documents


CHROMA_PATH = "./chroma"
COLLECTION_NAME = "documents"

_client = None
_collection = None


def get_client():
    global _client

    if _client is None:
        import chromadb

        _client = chromadb.PersistentClient(path=CHROMA_PATH)

    return _client


def get_collection():
    global _collection

    if _collection is None:
        _collection = get_client().get_or_create_collection(name=COLLECTION_NAME)

    return _collection


def reset_collection():
    global _collection

    client = get_client()
    try:
        client.delete_collection(name=COLLECTION_NAME)
    except Exception:
        pass

    _collection = client.get_or_create_collection(name=COLLECTION_NAME)
    return _collection


def index_documents() -> None:
    collection = reset_collection()
    documents = load_markdown_documents()
    chunks = chunk_documents(documents)

    if not chunks:
        return

    embeddings = embed_texts([chunk["content"] for chunk in chunks])
    ids = [f'{chunk["source"]}:{chunk["chunk_id"]}' for chunk in chunks]
    metadatas = [
        {
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"],
        }
        for chunk in chunks
    ]

    collection.add(
        ids=ids,
        documents=[chunk["content"] for chunk in chunks],
        embeddings=embeddings,
        metadatas=metadatas,
    )


def retrieve_chunks(question: str, top_k: int = 1) -> list[dict]:
    collection = get_collection()
    document_count = collection.count()
    if document_count == 0:
        return []

    question_embedding = embed_text(question)
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=min(top_k, document_count),
    )

    chunks = []
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    for content, metadata in zip(documents, metadatas):
        chunks.append(
            {
                "content": content,
                "source": metadata["source"],
            }
        )

    return chunks
