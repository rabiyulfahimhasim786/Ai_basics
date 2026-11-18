"""Lesson 02: LangChain agent with local Python tools."""
import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
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
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("Set OPENAI_API_KEY before running this lesson")
    return ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-5.5"), temperature=0)


STUDENTS = {101: {"name": "Arun", "department": "Computer Science", "semester": 5}}
ATTENDANCE = {101: {"attended": 85, "total": 100}}
FEES = {101: {"total": 50000, "paid": 40000, "pending": 10000}}


@tool
def get_student(student_id: int) -> dict:
    """Look up a student profile by college student ID."""
    return STUDENTS.get(student_id, {"error": "Student not found"})


@tool
def get_attendance(student_id: int) -> dict:
    """Get the number of classes attended and total classes for a student."""
    row = ATTENDANCE.get(student_id)
    if not row:
        return {"error": "Attendance not found"}
    return {**row, "percentage": round(row["attended"] / row["total"] * 100, 2)}


@tool
def get_fee_balance(student_id: int) -> dict:
    """Get total, paid, and pending tuition fees for a student."""
    return FEES.get(student_id, {"error": "Fee record not found"})


def main() -> None:
    agent = create_agent(
        model=build_chat_model(),
        tools=[get_student, get_attendance, get_fee_balance],
        system_prompt=(
            "You are a college assistant. Use tools for student facts. "
            "Never invent student records or claim a tool succeeded when it did not."
        ),
    )
    result = agent.invoke({"messages": [{"role": "user", "content": "Find student 101's attendance and pending fee."}]})
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
