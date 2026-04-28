CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


def chunk_document(document: dict, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[dict]:
    text = document["text"]
    source = document["source"]
    chunks = []
    start = 0
    chunk_id = 0

    while start < len(text):
        end = start + chunk_size
        content = text[start:end].strip()

        if content:
            chunks.append(
                {
                    "content": content,
                    "source": source,
                    "chunk_id": chunk_id,
                }
            )
            chunk_id += 1

        if end >= len(text):
            break

        start = end - overlap

    return chunks


def chunk_documents(documents: list[dict]) -> list[dict]:
    chunks = []

    for document in documents:
        chunks.extend(chunk_document(document))

    return chunks
