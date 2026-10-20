from app.rag.chunking import chunk_text


def test_short_text_is_one_chunk() -> None:
    assert chunk_text("checkout timed out", chunk_size=500, overlap=80) == ["checkout timed out"]


def test_overlap_keeps_boundary_words() -> None:
    text = "A" * 40 + " TIMEOUT " + "B" * 40
    chunks = chunk_text(text, chunk_size=50, overlap=15)
    assert len(chunks) >= 2
    assert any("TIMEOUT" in chunk for chunk in chunks)
