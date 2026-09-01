from typing import TypedDict

from langgraph.graph import (
    END,
    START,
    StateGraph,
)

from app.services.rag import (
    RAGService
)


class RAGState(TypedDict, total=False):

    collection_id: str

    question: str

    top_k: int

    rewritten_query: str

    answer: str

    sources: list

    grounded: bool

    confidence: float


rag = RAGService()


# ======================================
# REWRITE
# ======================================

def rewrite_node(
    state: RAGState
):

    rewritten = (
        rag.rewrite_query(
            state["question"]
        )
    )

    return {

        "rewritten_query":
            rewritten
    }


# ======================================
# RETRIEVE
# ======================================

def retrieve_node(
    state: RAGState
):

    ranked = rag.retrieve(

        state["collection_id"],

        state["rewritten_query"],

        state.get(
            "top_k",
            5
        )
    )

    sources = [

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
                float(score),

            "text":
                doc.page_content,
        }

        for doc, score in ranked
    ]

    return {

        "sources":
            sources
    }


# ======================================
# GENERATE
# ======================================

def generate_node(
    state: RAGState
):

    result = rag.answer(

        state["collection_id"],

        state["question"],

        state.get(
            "top_k",
            5
        )
    )

    return {

        "answer":
            result["answer"],

        "grounded":
            result["grounded"],

        "confidence":
            result["confidence"],
    }


# ======================================
# GRAPH
# ======================================

def build_graph():

    graph = StateGraph(
        RAGState
    )

    graph.add_node(
        "rewrite",
        rewrite_node
    )

    graph.add_node(
        "retrieve",
        retrieve_node
    )

    graph.add_node(
        "generate",
        generate_node
    )

    graph.add_edge(
        START,
        "rewrite"
    )

    graph.add_edge(
        "rewrite",
        "retrieve"
    )

    graph.add_edge(
        "retrieve",
        "generate"
    )

    graph.add_edge(
        "generate",
        END
    )

    return graph.compile()


rag_graph = build_graph()
