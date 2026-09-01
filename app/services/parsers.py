from pathlib import Path
import re

from pypdf import PdfReader


SUPPORTED = {
    ".pdf",
    ".txt",
    ".md",
    ".markdown",
}


def clean_text(text: str) -> str:

    text = text.replace(
        "\x00",
        " "
    )

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()


def parse_file(path: Path) -> str:

    suffix = path.suffix.lower()

    # PDF
    if suffix == ".pdf":

        reader = PdfReader(
            str(path)
        )

        pages = []

        for i, page in enumerate(
            reader.pages,
            start=1
        ):

            content = (
                page.extract_text()
                or ""
            )

            if content.strip():

                pages.append(
                    f"[Page {i}]\n{content}"
                )

        return clean_text(
            "\n\n".join(pages)
        )

    # TXT / Markdown
    if suffix in {
        ".txt",
        ".md",
        ".markdown",
    }:

        return clean_text(
            path.read_text(
                encoding="utf-8",
                errors="ignore"
            )
        )

    raise ValueError(
        f"Unsupported file type: {suffix}"
    )
