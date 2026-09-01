import re

from collections import Counter


def _tokens(text: str):

    return re.findall(
        r"\b[a-zA-Z0-9_]{2,}\b",
        text.lower()
    )


def lexical_score(
    query: str,
    text: str
) -> float:

    query_tokens = Counter(
        _tokens(query)
    )

    document_tokens = Counter(
        _tokens(text)
    )

    if (
        not query_tokens
        or not document_tokens
    ):

        return 0.0

    overlap = sum(
        min(
            query_tokens[token],
            document_tokens[token]
        )
        for token in query_tokens
    )

    return (
        overlap /
        max(
            1,
            sum(query_tokens.values())
        )
    )


def rerank(
    query: str,
    docs_and_scores: list,
    top_k: int,
):

    ranked = []

    for doc, vector_score in (
        docs_and_scores
    ):

        lexical = lexical_score(
            query,
            doc.page_content
        )

        score = (
            0.70 *
            float(vector_score)
            +
            0.30 *
            lexical
        )

        ranked.append(
            (
                doc,
                score
            )
        )

    ranked.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return ranked[:top_k]
