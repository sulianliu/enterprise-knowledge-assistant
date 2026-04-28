from backend.api import query as query_api


def test_query_returns_generated_answer_with_unique_sorted_sources(monkeypatch):
    chunks = [
        {
            "content": "First policy chunk",
            "source": "benefits.md",
        },
        {
            "content": "Second policy chunk",
            "source": "handbook.md",
        },
        {
            "content": "Repeated source chunk",
            "source": "benefits.md",
        },
    ]
    generated_prompts = []

    monkeypatch.setattr(query_api, "retrieve_chunks", lambda question: chunks)
    monkeypatch.setattr(
        query_api,
        "build_prompt",
        lambda context, question: f"context={context}; question={question}",
    )

    def fake_generate_answer(prompt):
        generated_prompts.append(prompt)
        return "Use the benefits policy."

    monkeypatch.setattr(query_api, "generate_answer", fake_generate_answer)

    response = query_api.query(query_api.QueryRequest(question="What benefits exist?"))

    assert response.answer == "Use the benefits policy."
    assert response.sources == ["benefits.md", "handbook.md"]
    assert generated_prompts == [
        "context=First policy chunk\n\nSecond policy chunk\n\nRepeated source chunk; "
        "question=What benefits exist?"
    ]


def test_query_returns_i_do_not_know_without_sources_when_no_chunks(monkeypatch):
    monkeypatch.setattr(query_api, "retrieve_chunks", lambda question: [])

    def fail_generate_answer(prompt):
        raise AssertionError("LLM should not be called without retrieved context")

    monkeypatch.setattr(query_api, "generate_answer", fail_generate_answer)

    response = query_api.query(query_api.QueryRequest(question="Unknown?"))

    assert response.answer == "I don't know"
    assert response.sources == []
