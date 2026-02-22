# app/services/llm_factory.py

from langchain_groq import ChatGroq
from app.config import settings


def get_vision_model():
    return ChatGroq(
        groq_api_key=settings.GROQ_API_KEY,
        model=settings.LARGE_VISION_MODEL,
        temperature=0
    )


def get_small_llm():
    return ChatGroq(
        groq_api_key=settings.GROQ_API_KEY,
        model=settings.SMALL_LLM_MODEL,
        temperature=0
    )