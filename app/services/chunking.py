from dataclasses import dataclass
import re


@dataclass
class Chunk:

    chunk_id: str

    text: str

    start: int

    end: int


def chunk_text(
    text: str,
    chunk_size: int = 900,
    overlap: int = 150,
) -> list[Chunk]:

    if not text.strip():

        return []

    if overlap >= chunk_size:

        raise ValueError(
            "chunk_overlap must be "
            "smaller than chunk_size"
        )

    paragraphs = [
        p.strip()
        for p in re.split(
            r"\n\s*\n",
            text
        )
        if p.strip()
    ]

    chunks = []

    buffer = ""

    cursor = 0

    for paragraph in paragraphs:

        candidate = (
            f"{buffer}\n\n{paragraph}".strip()
            if buffer
            else paragraph
        )

        if len(candidate) <= chunk_size:

            buffer = candidate

            continue

        if buffer:

            start = text.find(
                buffer,
                cursor
            )

            if start < 0:
                start = cursor

            end = start + len(buffer)

            chunks.append(
                Chunk(
                    chunk_id=(
                        f"chunk-{len(chunks):05d}"
                    ),
                    text=buffer,
                    start=start,
                    end=end,
                )
            )

            cursor = end

        # Handle very large paragraphs
        if len(paragraph) > chunk_size:

            step = (
                chunk_size - overlap
            )

            for start_local in range(
                0,
                len(paragraph),
                step,
            ):

                part = paragraph[
                    start_local:
                    start_local + chunk_size
                ].strip()

                if not part:
                    continue

                chunks.append(
                    Chunk(
                        chunk_id=(
                            f"chunk-{len(chunks):05d}"
                        ),
                        text=part,
                        start=(
                            cursor +
                            start_local
                        ),
                        end=(
                            cursor +
                            start_local +
                            len(part)
                        ),
                    )
                )

            buffer = ""

            cursor += len(paragraph)

        else:

            tail = (
                buffer[-overlap:]
                if buffer
                else ""
            )

            buffer = (
                f"{tail}\n\n{paragraph}"
                .strip()
            )

    if buffer:

        start = text.find(
            buffer,
            cursor
        )

        if start < 0:

            start = max(
                0,
                cursor
            )

        chunks.append(
            Chunk(
                chunk_id=(
                    f"chunk-{len(chunks):05d}"
                ),
                text=buffer,
                start=start,
                end=start + len(buffer),
            )
        )

    return chunks
