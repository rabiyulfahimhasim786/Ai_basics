# Python AI Engineering – Learning Repository

A progressive, runnable learning path for **LLM, AI Agents, MCP, LangChain, RAG and Vector Databases**, followed by a FastAPI + Pydantic college-management assistant.

## Learning order

1. `01_LLM` – call an LLM with the OpenAI Responses API, or an OpenRouter model through the OpenAI-compatible Chat Completions API.
2. `02_AI_Agent` – let an agent select and call Python tools.
3. `03_MCP` – expose college functions through an MCP server.
4. `04_LangChain` – build a prompt/model chain.
5. `05_RAG` – retrieve policy chunks and ground an answer.
6. `06_Vector_Database` – embed, store and search documents in Qdrant Cloud.
7. `07_Agentic_AI` – build a bounded multi-step workflow with planning stages, deterministic checks and an LLM summary.
8. `08_College_Management_Integrated` – combine the modules with FastAPI, Pydantic, SQLite, LangChain agents, MCP and Qdrant Cloud.

## Prerequisites

- Python 3.11 or newer
- OpenAI API key and/or an OpenRouter API key (select with `LLM_PROVIDER=openai|openrouter`)
- Qdrant Cloud cluster URL and API key (only for vector/RAG/integrated lessons)

All lessons use the OpenAI Python SDK or `langchain-openai`. OpenRouter is supported without another package because it exposes an OpenAI-compatible API. Embeddings still use OpenAI, so RAG and vector lessons require `OPENAI_API_KEY` even when the chat model uses OpenRouter.

Create a virtual environment and install the dependencies for the lesson you are running. For the integrated project, follow its own README.

## LLM providers

Each LLM lesson reads `LLM_PROVIDER` from its own `.env` file:

- `openai` (default): uses `OPENAI_API_KEY` and `OPENAI_MODEL`.
- `openrouter`: uses `OPENROUTER_API_KEY`, `OPENROUTER_MODEL` (default `nvidia/nemotron-3-ultra-550b-a55b:free`), and `OPENROUTER_BASE_URL` (default `https://openrouter.ai/api/v1`).

OpenRouter exposes an OpenAI-compatible Chat Completions API, so the same `openai` and `langchain-openai` packages work with either provider. Embeddings still use OpenAI: lessons 05, 06 and 08 need `OPENAI_API_KEY` for embeddings, while lessons 05 and 08 can still use OpenRouter for the chat/answer model.

> Never commit `.env`, API keys, database files containing real student data, or Qdrant credentials.

## Design principle

SQLite stores structured transactional records (students, attendance, fees). Qdrant stores embeddings and document payloads (college policies). They are different systems and are not interchangeable.
