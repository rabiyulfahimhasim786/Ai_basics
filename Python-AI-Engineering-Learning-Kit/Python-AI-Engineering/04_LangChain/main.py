"""Lesson 04: prompt -> model chain."""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_DEFAULT_MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"


def build_chat_model() -> ChatOpenAI:
    provider = os.getenv("LLM_PROVIDER", "openai").strip().lower()
    if provider == "openrouter":
        if not os.getenv("OPENROUTER_API_KEY"):
            raise RuntimeError("Set OPENROUTER_API_KEY before running this lesson")
        return ChatOpenAI(
            model=os.getenv("OPENROUTER_MODEL", OPENROUTER_DEFAULT_MODEL),
            api_key=os.environ["OPENROUTER_API_KEY"],
            base_url=os.getenv("OPENROUTER_BASE_URL", OPENROUTER_BASE_URL),
            temperature=0,
        )
    if provider != "openai":
        raise RuntimeError(f"Unsupported LLM_PROVIDER: {provider!r}")
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("Set OPENAI_API_KEY before running this lesson")
    return ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-5.5"), temperature=0)


def main() -> None:
    model = build_chat_model()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a college academic support assistant. Be concise and do not invent policy."),
        ("human", "Question: {question}"),
    ])
    chain = prompt | model
    response = chain.invoke({"question": "Explain the difference between a semester and a credit."})
    print(response.content)


if __name__ == "__main__":
    main()
