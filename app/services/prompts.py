from langchain_core.prompts import (
    ChatPromptTemplate
)


REWRITE_PROMPT = ChatPromptTemplate.from_messages(

    [

        (
            "system",

            """
Rewrite the user's question into
a concise retrieval query.

Preserve:

- Important entities
- Dates
- Technical terms
- Constraints
- Names

Return ONLY the rewritten query.
"""
        ),

        (
            "human",
            "{question}"
        ),
    ]
)


ANSWER_PROMPT = ChatPromptTemplate.from_messages(

    [

        (
            "system",

            """
You are a grounded document
question-answering assistant.

Rules:

1. Answer ONLY using the supplied context.

2. If the context does not contain
enough information, say:

"I couldn't find enough information
in the uploaded documents."

3. Never invent facts.

4. Never invent citations.

5. Keep the answer clear and useful.

6. Cite supporting chunks using:

[Source 1]

[Source 2]

etc.

7. Only cite a source if it supports
the statement.

Context:

{context}
"""
        ),

        (
            "human",
            "Question: {question}"
        ),
    ]
)
