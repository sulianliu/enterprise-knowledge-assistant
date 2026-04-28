from backend.rag.ingest import load_markdown_documents


def test_load_markdown_documents_reads_non_empty_markdown_files_in_name_order(tmp_path):
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "b.md").write_text("  Bravo document  ", encoding="utf-8")
    (docs_dir / "a.md").write_text("# Alpha document\n", encoding="utf-8")
    (docs_dir / "empty.md").write_text("   \n", encoding="utf-8")
    (docs_dir / "notes.txt").write_text("Ignore me", encoding="utf-8")

    documents = load_markdown_documents(docs_dir)

    assert documents == [
        {
            "text": "# Alpha document",
            "source": "a.md",
        },
        {
            "text": "Bravo document",
            "source": "b.md",
        },
    ]


def test_load_markdown_documents_returns_empty_list_for_missing_directory(tmp_path):
    documents = load_markdown_documents(tmp_path / "missing")

    assert documents == []
