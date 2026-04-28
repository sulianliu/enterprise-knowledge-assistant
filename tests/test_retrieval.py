from backend.rag import retrieval


class FakeCollection:
    def __init__(self):
        self.add_call = None
        self.query_call = None
        self._count = 2

    def add(self, ids, documents, embeddings, metadatas):
        self.add_call = {
            "ids": ids,
            "documents": documents,
            "embeddings": embeddings,
            "metadatas": metadatas,
        }

    def count(self):
        return self._count

    def query(self, query_embeddings, n_results):
        self.query_call = {
            "query_embeddings": query_embeddings,
            "n_results": n_results,
        }
        return {
            "documents": [["Chunk one", "Chunk two"]],
            "metadatas": [[{"source": "a.md"}, {"source": "b.md"}]],
        }


def test_index_documents_resets_collection_and_preserves_metadata(monkeypatch):
    fake_collection = FakeCollection()
    documents = [
        {
            "text": "alpha bravo",
            "source": "handbook.md",
        }
    ]
    chunks = [
        {
            "content": "alpha",
            "source": "handbook.md",
            "chunk_id": 0,
        },
        {
            "content": "bravo",
            "source": "handbook.md",
            "chunk_id": 1,
        },
    ]

    monkeypatch.setattr(retrieval, "reset_collection", lambda: fake_collection)
    monkeypatch.setattr(retrieval, "load_markdown_documents", lambda: documents)
    monkeypatch.setattr(retrieval, "chunk_documents", lambda value: chunks)
    monkeypatch.setattr(retrieval, "embed_texts", lambda texts: [[0.1], [0.2]])

    retrieval.index_documents()

    assert fake_collection.add_call == {
        "ids": ["handbook.md:0", "handbook.md:1"],
        "documents": ["alpha", "bravo"],
        "embeddings": [[0.1], [0.2]],
        "metadatas": [
            {
                "source": "handbook.md",
                "chunk_id": 0,
            },
            {
                "source": "handbook.md",
                "chunk_id": 1,
            },
        ],
    }


def test_index_documents_resets_collection_without_adding_when_no_chunks(monkeypatch):
    fake_collection = FakeCollection()

    monkeypatch.setattr(retrieval, "reset_collection", lambda: fake_collection)
    monkeypatch.setattr(retrieval, "load_markdown_documents", lambda: [])
    monkeypatch.setattr(retrieval, "chunk_documents", lambda value: [])

    retrieval.index_documents()

    assert fake_collection.add_call is None


def test_retrieve_chunks_embeds_question_and_limits_top_k_to_collection_count(monkeypatch):
    fake_collection = FakeCollection()

    monkeypatch.setattr(retrieval, "get_collection", lambda: fake_collection)
    monkeypatch.setattr(retrieval, "embed_text", lambda text: [0.9, 0.8])

    chunks = retrieval.retrieve_chunks("What changed?", top_k=3)

    assert fake_collection.query_call == {
        "query_embeddings": [[0.9, 0.8]],
        "n_results": 2,
    }
    assert chunks == [
        {
            "content": "Chunk one",
            "source": "a.md",
        },
        {
            "content": "Chunk two",
            "source": "b.md",
        },
    ]


def test_retrieve_chunks_returns_empty_list_when_collection_is_empty(monkeypatch):
    fake_collection = FakeCollection()
    fake_collection._count = 0

    monkeypatch.setattr(retrieval, "get_collection", lambda: fake_collection)

    assert retrieval.retrieve_chunks("Anything?") == []
    assert fake_collection.query_call is None
