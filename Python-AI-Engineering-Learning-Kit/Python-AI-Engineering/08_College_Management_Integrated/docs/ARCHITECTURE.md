# Architecture and request flow

```text
Client
  |
  v
FastAPI endpoint -- Pydantic validates request
  |
  v
LangChain Agent + OpenAI model
  |                         |
  | student/attendance/fees  | college-policy question
  v                         v
MCP client                RAG tool
  |                         |
  v                         v
MCP server               Retriever
  |                         |
  v                         v
SQLAlchemy + SQLite      Embeddings + Qdrant Cloud
  |                         |
  +-----------+-------------+
              |
              v
        LLM final response
              |
              v
       Pydantic response
```

## Responsibilities

- **LLM:** language understanding and response generation.
- **Agent:** chooses whether to call tools and which tools to call.
- **MCP:** standard protocol for discovering and invoking remote tools/resources.
- **LangChain:** model, prompt, tool and agent orchestration abstractions.
- **RAG:** retrieves relevant policy context before answer generation.
- **Qdrant:** stores/searches vector representations and metadata.
- **SQLite:** stores authoritative structured student records.

## Security work required before production

1. Add authentication and authorization; scope every student query to the authenticated principal.
2. Add database migrations (Alembic), indexes, constraints and transaction handling.
3. Authenticate and authorize MCP clients; do not expose the demo server publicly.
4. Add Qdrant collection access controls and tenant/department filters where needed.
5. Add rate limits, timeouts, retries, request tracing, audit logs and usage budgets.
6. Validate tool arguments and tool results; never give the agent arbitrary SQL or unrestricted write tools.
7. Treat retrieved text as untrusted data and protect against prompt injection.
8. Add tests for authorization, retrieval quality, tool selection and model failures.
