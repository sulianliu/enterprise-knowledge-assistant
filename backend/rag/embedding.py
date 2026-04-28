import json
import os
from urllib.request import Request, urlopen


OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3"


def post_json(path: str, payload: dict) -> dict:
    url = f"{OLLAMA_BASE_URL}{path}"
    data = json.dumps(payload).encode("utf-8")
    request = Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urlopen(request, timeout=120) as response:
        return json.loads(response.read().decode("utf-8"))


def embed_texts(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []

    response = post_json(
        "/api/embed",
        {
            "model": EMBEDDING_MODEL,
            "input": texts,
        },
    )

    return response["embeddings"]


def embed_text(text: str) -> list[float]:
    return embed_texts([text])[0]


def generate_answer(prompt: str) -> str:
    response = post_json(
        "/api/generate",
        {
            "model": LLM_MODEL,
            "prompt": prompt,
            "stream": False,
        },
    )

    return response.get("response", "").strip()
