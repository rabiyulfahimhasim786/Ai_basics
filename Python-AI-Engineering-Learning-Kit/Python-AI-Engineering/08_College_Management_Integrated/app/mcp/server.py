"""Standalone MCP server. It reads the same SQLite database as FastAPI."""
from mcp.server.fastmcp import FastMCP
from app.db.database import Base, engine, SessionLocal
from app.services.college_service import student_details as read_student, attendance_details as read_attendance, fee_details as read_fee

Base.metadata.create_all(bind=engine)
mcp = FastMCP("college-management-tools", host="127.0.0.1", port=8001)


@mcp.tool()
def student_details(student_id: int) -> dict:
    """Get a college student profile by student ID."""
    with SessionLocal() as db:
        return read_student(db, student_id)


@mcp.tool()
def attendance_details(student_id: int) -> dict:
    """Get attended classes, total classes, and attendance percentage for a student."""
    with SessionLocal() as db:
        return read_attendance(db, student_id)


@mcp.tool()
def fee_details(student_id: int) -> dict:
    """Get total fees, paid fees, and pending fee balance for a student."""
    with SessionLocal() as db:
        return read_fee(db, student_id)


@mcp.resource("college://attendance-policy")
def attendance_policy() -> str:
    """A short sample attendance policy. Consult the official handbook for binding rules."""
    return "Sample learning policy: minimum attendance is 75%. Condonation and exceptions depend on official college regulations."


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
