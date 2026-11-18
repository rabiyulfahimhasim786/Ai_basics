# 05 – RAG (Retrieval-Augmented Generation)

**Goal:** Split a policy document into chunks, retrieve relevant chunks, and ask the LLM to answer from that context. The vector store is Qdrant Cloud in this course.

Set `OPENAI_API_KEY`, `QDRANT_URL`, and `QDRANT_API_KEY`. Run `python main.py` from this folder. It ingests the included sample policy and answers a sample question.

To use OpenRouter for the answering model, add `LLM_PROVIDER=openrouter`, `OPENROUTER_API_KEY`, and `OPENROUTER_MODEL` (for example `nvidia/nemotron-3-ultra-550b-a55b:free`). Embeddings still use OpenAI, so `OPENAI_API_KEY` is required either way.

RAG reduces unsupported answers but does not guarantee correctness. Evaluate retrieval quality and cite the source chunks in production.
