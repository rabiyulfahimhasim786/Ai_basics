# 4-week learning plan

## Week 1 – LLM and API foundations
- Run `01_LLM` and inspect the Responses API call.
- Learn system instructions, user input, tokens, context windows and model errors.
- Learn Pydantic request/response models and add a simple FastAPI endpoint.
- Exercise: return a Pydantic structured response and validate it.

## Week 2 – LangChain and agents
- Run `04_LangChain` and trace prompt -> model.
- Run `02_AI_Agent`; inspect tool docstrings and tool invocation.
- Exercise: add a `get_student` tool and a deterministic attendance calculation.
- Learn the difference between a chain and an agent.

## Week 3 – Embeddings, vector DB and RAG
- Run `06_Vector_Database`; compare similarity results for differently worded questions.
- Run `05_RAG`; inspect retrieved chunks before looking at the final answer.
- Exercise: add a second policy document and include source metadata.
- Learn chunk size, overlap, top-k, similarity score, embedding dimension and filters.

## Week 4 – MCP and integration
- Run `03_MCP`; inspect tools and resources with an MCP client/Inspector.
- Read the integrated project architecture and run the MCP server separately.
- Seed SQLite, ingest policies into Qdrant, then start FastAPI.
- Exercise: add a new read-only MCP tool and test it through `/api/v1/chat`.
- Final: add auth, tests, Docker and observability as separate production-hardening tasks.
