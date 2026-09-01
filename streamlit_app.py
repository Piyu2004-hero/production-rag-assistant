import os

import requests
import streamlit as st


API_URL = os.getenv(
    "API_URL",
    "http://localhost:8000"
)


st.set_page_config(

    page_title=(
        "Production RAG Assistant"
    ),

    page_icon="🧠",

    layout="wide",
)


st.title(
    "🧠 Production-Style RAG Assistant"
)

st.caption(
    "PDF • TXT • Markdown | "
    "FAISS | RAG | FastAPI"
)


if "collection_id" not in st.session_state:

    st.session_state.collection_id = None


# ======================================
# SIDEBAR
# ======================================

with st.sidebar:

    st.header(
        "1. Upload Documents"
    )

    uploaded = st.file_uploader(

        "Choose PDF, TXT or Markdown files",

        type=[
            "pdf",
            "txt",
            "md",
            "markdown"
        ],

        accept_multiple_files=True,
    )

    if st.button(
        "Build / Index Documents",
        type="primary"
    ):

        if not uploaded:

            st.error(
                "Please upload at least "
                "one document."
            )

        else:

            files = [

                (

                    "files",

                    (
                        f.name,

                        f.getvalue(),

                        f.type
                        or
                        "application/octet-stream"
                    )
                )

                for f in uploaded
            ]

            try:

                with st.spinner(

                    "Parsing, chunking, "
                    "embedding and indexing..."
                ):

                    response = requests.post(

                        f"{API_URL}"
                        "/documents/upload",

                        files=files,

                        timeout=300,
                    )

                if response.ok:

                    data = (
                        response.json()
                    )

                    st.session_state.collection_id = (
                        data[
                            "collection_id"
                        ]
                    )

                    st.success(

                        f"Indexed "
                        f"{len(data['documents'])} "
                        f"document(s)."
                    )

                    for doc in (
                        data["documents"]
                    ):

                        st.write(

                            f"**{doc['filename']}** "
                            f"— {doc['chunks']} chunks"
                        )

                else:

                    st.error(
                        response.text
                    )

            except requests.RequestException as exc:

                st.error(
                    f"API connection error: {exc}"
                )

    st.divider()

    st.write(
        "**Collection ID**"
    )

    st.code(

        st.session_state.collection_id
        or
        "Upload documents first"
    )


# ======================================
# QUESTION
# ======================================

st.header(
    "2. Ask a Question"
)


question = st.text_area(

    "Question",

    placeholder=(
        "Ask something that can be "
        "answered from the uploaded "
        "documents..."
    ),

    height=120,
)


top_k = st.slider(

    "Retrieved sources",

    1,

    10,

    5
)


if st.button(

    "Ask",

    type="primary",

    use_container_width=True
):

    if not st.session_state.collection_id:

        st.warning(
            "Upload and index "
            "documents first."
        )

    elif not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        payload = {

            "collection_id":
                st.session_state.collection_id,

            "question":
                question.strip(),

            "top_k":
                top_k,
        }

        try:

            with st.spinner(

                "Rewriting query and "
                "retrieving context..."
            ):

                response = requests.post(

                    f"{API_URL}/query",

                    json=payload,

                    timeout=180,
                )

            if response.ok:

                data = (
                    response.json()
                )

                st.subheader(
                    "Answer"
                )

                st.markdown(
                    data["answer"]
                )

                col1, col2 = (
                    st.columns(2)
                )

                col1.metric(

                    "Grounded",

                    (
                        "Yes"
                        if data.get("grounded", False)
                        else
                        "Review"
                    )
                )

                col2.metric(

                    "Confidence",

                    f"{data.get('confidence', 0.0):.2f}"
                )

                with st.expander(
                    "Query Rewriting"
                ):

                    st.code(
                        data[
                            "rewritten_query"
                        ]
                    )

                st.subheader(
                    "Sources"
                )

                for i, source in enumerate(

                    data["sources"],

                    1
                ):

                    with st.expander(

                        f"[Source {i}] "
                        f"{source['filename']} "
                        f"• "
                        f"{source['chunk_id']} "
                        f"• "
                        f"score="
                        f"{source['score']:.3f}"
                    ):

                        st.write(
                            source["text"]
                        )

            else:

                st.error(
                    response.text
                )

        except requests.RequestException as exc:

            st.error(
                f"API connection error: {exc}"
            )


st.divider()

st.caption(

    "Upload → Parse → Clean → Chunk → "
    "Embed → FAISS → Rewrite → Retrieve → "
    "Rerank → Grounded LLM → Validate → Sources"
)
