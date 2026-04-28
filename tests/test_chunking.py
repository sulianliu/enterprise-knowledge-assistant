from backend.rag.chunking import chunk_document, chunk_documents


def test_chunk_document_preserves_source_and_assigns_incrementing_chunk_ids():
    document = {
        "text": "abcdefghijkl",
        "source": "handbook.md",
    }

    chunks = chunk_document(document, chunk_size=5, overlap=2)

    assert chunks == [
        {
            "content": "abcde",
            "source": "handbook.md",
            "chunk_id": 0,
        },
        {
            "content": "defgh",
            "source": "handbook.md",
            "chunk_id": 1,
        },
        {
            "content": "ghijk",
            "source": "handbook.md",
            "chunk_id": 2,
        },
        {
            "content": "jkl",
            "source": "handbook.md",
            "chunk_id": 3,
        },
    ]


def test_chunk_documents_combines_chunks_from_all_documents():
    documents = [
        {
            "text": "alpha",
            "source": "a.md",
        },
        {
            "text": "bravo",
            "source": "b.md",
        },
    ]

    chunks = chunk_documents(documents)

    assert chunks == [
        {
            "content": "alpha",
            "source": "a.md",
            "chunk_id": 0,
        },
        {
            "content": "bravo",
            "source": "b.md",
            "chunk_id": 0,
        },
    ]
