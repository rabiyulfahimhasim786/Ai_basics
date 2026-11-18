# 02 – AI Agent and tools

**Goal:** See how an agent chooses and calls Python functions. The tools use mock data so the lesson is safe to run.

Install `langchain`, `langchain-openai`, and `python-dotenv`; set `OPENAI_API_KEY` and optionally `OPENAI_MODEL`. To use OpenRouter instead, set `LLM_PROVIDER=openrouter`, `OPENROUTER_API_KEY`, and `OPENROUTER_MODEL` (for example `nvidia/nemotron-3-ultra-550b-a55b:free`). See `.env.example`.

Run `python main.py`.

Try asking for student 101's attendance and fee balance. Inspect the tool docstrings: they help the model understand when a tool should be used.
