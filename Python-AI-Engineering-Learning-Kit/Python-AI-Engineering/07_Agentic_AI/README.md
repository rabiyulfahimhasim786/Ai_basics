# 07 – Agentic AI workflow

**Agent vs Agentic AI:** An AI agent is an executing component that can reason and use tools. Agentic AI describes a broader system that can pursue a goal through multiple steps, maintain state, evaluate results and decide what to do next. It is not a separate model or one Python package.

This example demonstrates a bounded, auditable multi-step workflow: gather student facts, calculate eligibility deterministically, then ask the LLM to explain the verified result. The business rule is Python code, not an LLM guess.

Install `openai`, `python-dotenv`, and `langchain-openai`; set `OPENAI_API_KEY` and optionally `OPENAI_MODEL`. To use OpenRouter instead, set `LLM_PROVIDER=openrouter`, `OPENROUTER_API_KEY`, and `OPENROUTER_MODEL` (for example `nvidia/nemotron-3-ultra-550b-a55b:free`). See `.env.example`. Run `python main.py`.

## Exercise

Add a step that retrieves the official policy from RAG. Add a maximum-step limit and record each workflow event in a trace list.
