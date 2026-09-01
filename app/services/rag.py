import re

from app.config import get_settings

from app.services.llm import (
    get_llm
)

from app.services.prompts import (
    ANSWER_PROMPT,
    REWRITE_PROMPT
)

from app.services.reranker import (
    rerank
)

from app.services.vector_store import (
    VectorStoreManager
)


class RAGService:

    def __init__(self):

        self.settings = get_settings()

        self.stores = (
            VectorStoreManager()
        )

    # --------------------------------
    # QUERY REWRITING
    # --------------------------------

    def rewrite_query(
        self,
        question: str
    ) -> str:

        chain = (
            REWRITE_PROMPT
            | get_llm()
        )

        response = chain.invoke(

            {
                "question":
                    question
            }
        )

        text = (
            response.content
            if hasattr(
                response,
                "content"
            )
            else str(response)
        )

        return (
            text.strip()
            or question
        )

    # --------------------------------
    # RETRIEVAL
    # --------------------------------

    def retrieve(
        self,
        collection_id: str,
        query: str,
        top_k: int
    ):

        store = (
            self.stores.load(
                collection_id
            )
        )

        candidates = (
            store
            .similarity_search_with_score(

                query,

                k=max(
                    top_k,
                    self.settings.retrieval_k
                )
            )
        )

        converted = []

        for doc, distance in candidates:

            vector_score = (
                1.0 /
                (
                    1.0 +
                    float(distance)
                )
            )

            converted.append(
                (
                    doc,
                    vector_score
                )
            )

        return rerank(

            query,

            converted,

            min(
                top_k,
                self.settings.rerank_k
            )
        )

    # --------------------------------
    # CONTEXT
    # --------------------------------

    @staticmethod
    def build_context(
        ranked_docs
    ):

        blocks = []

        for idx, (
            doc,
            score
        ) in enumerate(
            ranked_docs,
            start=1
        ):

            blocks.append(

                f"""
[Source {idx}]
File: {doc.metadata.get(
    'filename',
    'unknown'
)}

Chunk: {doc.metadata.get(
    'chunk_id',
    'unknown'
)}

Score: {score:.3f}

{doc.page_content}
"""
            )

        return "\n\n".join(
            blocks
        )

    # --------------------------------
    # GROUNDING VALIDATION
    # --------------------------------

    @staticmethod
    def validate_grounding(
        answer: str,
        source_count: int
    ) -> bool:

        if source_count == 0:

            return False

        if (
            "couldn't find enough information"
            in answer.lower()
        ):

            return False

        citations = re.findall(
            r"\[Source\s+\d+\]",
            answer
        )

        if not citations:

            return False

        for citation in citations:

            number = int(
                re.search(
                    r"\d+",
                    citation
                ).group()
            )

            if (
                number < 1
                or number > source_count
            ):

                return False

        return True

    # --------------------------------
    # NORMAL ANSWER
    # --------------------------------

    def answer(
        self,
        collection_id: str,
        question: str,
        top_k: int
    ):

        rewritten = (
            self.rewrite_query(
                question
            )
        )

        ranked = (
            self.retrieve(
                collection_id,
                rewritten,
                top_k
            )
        )

        context = (
            self.build_context(
                ranked
            )
        )

        context = context[
            :self.settings.max_context_chars
        ]

        chain = (
            ANSWER_PROMPT
            | get_llm()
        )

        response = chain.invoke(

            {
                "context":
                    context,

                "question":
                    question,
            }
        )

        answer = (

            response.content

            if hasattr(
                response,
                "content"
            )

            else str(response)
        )

        sources = []

        for doc, score in ranked:

            sources.append(

                {

                    "document_id":
                        doc.metadata.get(
                            "document_id",
                            ""
                        ),

                    "filename":
                        doc.metadata.get(
                            "filename",
                            ""
                        ),

                    "chunk_id":
                        doc.metadata.get(
                            "chunk_id",
                            ""
                        ),

                    "score":
                        round(
                            float(score),
                            4
                        ),

                    "text":
                        doc.page_content,
                }
            )

        confidence = round(

            sum(
                s["score"]
                for s in sources
            )
            /
            max(
                1,
                len(sources)
            ),

            4
        )

        return {

            "question":
                question,

            "rewritten_query":
                rewritten,

            "answer":
                answer.strip(),

            "sources":
                sources,

            "grounded":
                self.validate_grounding(
                    answer,
                    len(sources)
                ),

            "confidence":
                confidence,
        }

    # --------------------------------
    # STREAMING
    # --------------------------------

    def stream_answer(
        self,
        collection_id: str,
        question: str,
        top_k: int
    ):

        rewritten = (
            self.rewrite_query(
                question
            )
        )

        ranked = (
            self.retrieve(
                collection_id,
                rewritten,
                top_k
            )
        )

        context = (
            self.build_context(
                ranked
            )
        )

        context = context[
            :self.settings.max_context_chars
        ]

        chain = (
            ANSWER_PROMPT
            | get_llm()
        )

        for chunk in chain.stream(

            {
                "context":
                    context,

                "question":
                    question,
            }
        ):

            text = (

                chunk.content

                if hasattr(
                    chunk,
                    "content"
                )

                else str(chunk)
            )

            if text:

                yield (
                    text,
                    rewritten,
                    ranked
                )
