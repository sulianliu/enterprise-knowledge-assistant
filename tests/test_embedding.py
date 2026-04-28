from backend.rag import embedding


def test_embed_texts_calls_ollama_embedding_model(monkeypatch):
    calls = []

    def fake_post_json(path, payload):
        calls.append(
            {
                "path": path,
                "payload": payload,
            }
        )
        return {
            "embeddings": [[1.0, 2.0], [3.0, 4.0]],
        }

    monkeypatch.setattr(embedding, "post_json", fake_post_json)

    embeddings = embedding.embed_texts(["first", "second"])

    assert embeddings == [[1.0, 2.0], [3.0, 4.0]]
    assert calls == [
        {
            "path": "/api/embed",
            "payload": {
                "model": "nomic-embed-text",
                "input": ["first", "second"],
            },
        }
    ]


def test_embed_texts_returns_empty_list_without_api_call(monkeypatch):
    def fail_post_json(path, payload):
        raise AssertionError("Ollama should not be called for empty input")

    monkeypatch.setattr(embedding, "post_json", fail_post_json)

    assert embedding.embed_texts([]) == []


def test_generate_answer_calls_ollama_llm_model_and_strips_text(monkeypatch):
    calls = []

    def fake_post_json(path, payload):
        calls.append(
            {
                "path": path,
                "payload": payload,
            }
        )
        return {
            "response": "  Grounded answer  ",
        }

    monkeypatch.setattr(embedding, "post_json", fake_post_json)

    answer = embedding.generate_answer("prompt text")

    assert answer == "Grounded answer"
    assert calls == [
        {
            "path": "/api/generate",
            "payload": {
                "model": "llama3",
                "prompt": "prompt text",
                "stream": False,
            },
        }
    ]
