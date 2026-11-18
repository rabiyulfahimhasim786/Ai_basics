"""Lesson 01: a plain LLM call. No tools, database, or retrieval."""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_DEFAULT_MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"


def ask_openrouter(question: str) -> str:
    if not os.getenv("OPENROUTER_API_KEY"):
        raise RuntimeError(
            "Set OPENROUTER_API_KEY in your environment or .env file "
            "when LLM_PROVIDER=openrouter"
        )
    # OpenRouter exposes an OpenAI-compatible Chat Completions API.
    client = OpenAI(
        base_url=os.getenv("OPENROUTER_BASE_URL", OPENROUTER_BASE_URL),
        api_key=os.environ["OPENROUTER_API_KEY"],
    )
    response = client.chat.completions.create(
        model=os.getenv("OPENROUTER_MODEL", OPENROUTER_DEFAULT_MODEL),
        messages=[
            {
                "role": "system",
                "content": "You are a helpful college information assistant. Do not invent official college rules.",
            },
            {"role": "user", "content": question},
        ],
    )
    return response.choices[0].message.content or ""


def ask_openai(question: str) -> str:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("Set OPENAI_API_KEY in your environment or .env file")
    client = OpenAI()
    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5.5"),
        instructions="You are a helpful college information assistant. Do not invent official college rules.",
        input=question,
    )
    return response.output_text


def ask_llm(question: str) -> str:
    provider = os.getenv("LLM_PROVIDER", "openai").strip().lower()
    if provider == "openrouter":
        return ask_openrouter(question)
    if provider == "openai":
        return ask_openai(question)
    raise RuntimeError(f"Unsupported LLM_PROVIDER: {provider!r}. Use 'openai' or 'openrouter'.")


if __name__ == "__main__":
    print(ask_llm("Explain what attendance percentage means in simple terms."))
