# 01 – LLM fundamentals

**Goal:** Send a prompt to an LLM and inspect the generated text. This is not an agent: no external tools are available to the model.

## Setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install openai python-dotenv
```

Create `.env` from `.env.example` and choose a provider.

**Option A – OpenAI (default)**

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-5.5
```

**Option B – OpenRouter**

```env
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=...
OPENROUTER_MODEL=nvidia/nemotron-3-ultra-550b-a55b:free
```

OpenRouter uses the same OpenAI SDK, but points `base_url` at `https://openrouter.ai/api/v1` and uses the Chat Completions API. No extra package is needed.

Run `python main.py`.

## Exercise

Change the system instructions, ask the same question again, and compare how the answer changes. Then add a Pydantic response schema in a follow-up exercise.
