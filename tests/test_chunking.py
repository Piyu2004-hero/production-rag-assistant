from app.services.chunking import (
    chunk_text
)


def test_chunking_returns_chunks():

    text = (
        "Paragraph one.\n\n"
        +
        ("Long text " * 200)
    )

    chunks = chunk_text(

        text,

        chunk_size=100,

        overlap=20
    )

    assert chunks

    assert all(
        c.text.strip()
        for c in chunks
    )
