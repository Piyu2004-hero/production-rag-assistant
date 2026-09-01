from functools import lru_cache

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from app.config import get_settings


@lru_cache
def get_llm():

    settings = get_settings()

    if (
        settings.llm_provider.lower()
        == "openai"
    ):

        return ChatOpenAI(

            api_key=settings.openai_api_key,

            model=settings.llm_model,

            temperature=0,

            streaming=True,
        )

    return ChatGroq(

        api_key=settings.groq_api_key,

        model=settings.llm_model,

        temperature=0,

        streaming=True,
    )
