from pathlib import Path


DOCS_DIR = Path("data/docs")


def load_markdown_documents(docs_dir: Path = DOCS_DIR) -> list[dict]:
    documents = []

    if not docs_dir.exists():
        return documents

    for path in sorted(docs_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8").strip()
        if text:
            documents.append(
                {
                    "text": text,
                    "source": path.name,
                }
            )

    return documents
