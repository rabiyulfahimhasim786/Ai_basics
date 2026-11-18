# 07 – Integrated College Management AI Assistant

This is the capstone: **FastAPI + Pydantic v2 + SQLAlchemy + SQLite + LangChain Agent + MCP + RAG + Qdrant Cloud**.

## Architecture

- SQLite: students, attendance, fees (structured records).
- Qdrant Cloud: college policy chunks and embeddings (semantic retrieval).
- MCP server: exposes read-only student, attendance and fee tools.
- LangChain agent: chooses MCP tools and the policy-search tool.
- FastAPI: validates requests with Pydantic and exposes `/api/v1/chat`.

## 1. Configure

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Windows: copy .env.example .env
```

Set `OPENAI_API_KEY`, `QDRANT_URL`, and `QDRANT_API_KEY` in `.env`. Set `OPENAI_MODEL` to a model enabled for your API account.

To use OpenRouter for the chat/agent model instead, set:

```env
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=...
OPENROUTER_MODEL=nvidia/nemotron-3-ultra-550b-a55b:free
```

OpenRouter uses the OpenAI-compatible API at `https://openrouter.ai/api/v1`. Embeddings still use OpenAI (`OPENAI_API_KEY` and `EMBEDDING_MODEL`), because OpenRouter does not provide an embeddings endpoint.

## 2. Seed SQLite and ingest policy documents

```bash
python -m scripts.seed_database
python -m scripts.ingest_policies
```

The ingestion script creates the Qdrant collection if needed and upserts deterministic document IDs. Re-running it updates the same sample chunks instead of duplicating them.

## 3. Start two processes

Terminal 1 – MCP server:

```bash
python -m app.mcp.server
```

Terminal 2 – FastAPI:

```bash
uvicorn app.main:app --reload --port 8000
```

Swagger UI: http://127.0.0.1:8000/docs

## 4. Test

```bash
curl -X POST http://127.0.0.1:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"question":"What is student 101 attendance and pending fee?"}'
```

Try: `What is the minimum attendance for semester exams?`

## Notes

- The demo seed data is fictional. Do not use it as real student data.
- This capstone is a learning baseline, not production-ready: add authentication, per-user authorization, audit logs, rate limits, retries, tracing, migrations and secret management before deployment.
- MCP is hosted separately on port 8001; the FastAPI app is on port 8000.
