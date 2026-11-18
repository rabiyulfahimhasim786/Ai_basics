"""Lesson 07: a bounded multi-step agentic workflow."""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

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
    return ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-5.5"), temperature=0)


def llm_is_configured() -> bool:
    provider = os.getenv("LLM_PROVIDER", "openai").strip().lower()
    if provider == "openrouter":
        return bool(os.getenv("OPENROUTER_API_KEY"))
    if provider == "openai":
        return bool(os.getenv("OPENAI_API_KEY"))
    return False


# Mock read-only college services. Replace with repository/service calls in a real app.
STUDENTS = {101: {"name": "Arun", "department": "Computer Science", "semester": 5}}
ATTENDANCE = {101: {"attended": 85, "total": 100}}
FEES = {101: {"total": 50000, "paid": 40000}}


def run_academic_review(student_id: int) -> dict:
    trace: list[str] = []

    # Step 1 – gather facts
    student = STUDENTS.get(student_id)
    if not student:
        return {"status": "not_found", "trace": ["student_lookup: not_found"]}
    trace.append("student_lookup: success")

    attendance = ATTENDANCE.get(student_id)
    if not attendance or attendance["total"] <= 0:
        return {"status": "incomplete_data", "trace": trace + ["attendance_lookup: missing_or_invalid"]}
    percentage = round(attendance["attended"] / attendance["total"] * 100, 2)
    trace.append("attendance_lookup: success")

    fee = FEES.get(student_id)
    if not fee:
        return {"status": "incomplete_data", "trace": trace + ["fee_lookup: missing"]}
    pending = fee["total"] - fee["paid"]
    trace.append("fee_lookup: success")

    # Step 2 – apply deterministic business rules (never delegate arithmetic/eligibility to LLM)
    attendance_threshold = 75.0
    attendance_check = percentage >= attendance_threshold
    trace.append("eligibility_rule: evaluated")

    facts = {
        "student": student,
        "attendance_percentage": percentage,
        "attendance_threshold": attendance_threshold,
        "attendance_check": attendance_check,
        "pending_fee": pending,
    }

    # Step 3 – generate a readable explanation from verified facts
    if not llm_is_configured():
        explanation = (
            "Set OPENAI_API_KEY, or set LLM_PROVIDER=openrouter with OPENROUTER_API_KEY, "
            "to generate a natural-language explanation."
        )
    else:
        model = build_chat_model()
        response = model.invoke(
            "Explain this verified college review clearly. Do not change the numbers or "
            "make a final examination decision. State that the college's official rules apply.\n"
            f"Verified facts: {facts}"
        )
        explanation = response.content
    trace.append("llm_summary: completed")

    return {"status": "completed", "facts": facts, "explanation": explanation, "trace": trace}


if __name__ == "__main__":
    import json
    print(json.dumps(run_academic_review(101), indent=2))
