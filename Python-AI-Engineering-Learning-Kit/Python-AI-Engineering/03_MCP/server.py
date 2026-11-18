"""Lesson 03: a small MCP server exposing college tools."""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("college-learning-server", host="127.0.0.1", port=8001)

STUDENTS = {101: {"name": "Arun", "department": "Computer Science", "semester": 5}}
ATTENDANCE = {101: {"attended": 85, "total": 100}}


@mcp.tool()
def student_details(student_id: int) -> dict:
    """Return a student profile by student ID."""
    return STUDENTS.get(student_id, {"error": "Student not found"})


@mcp.tool()
def attendance_details(student_id: int) -> dict:
    """Return attendance counts and percentage for a student."""
    row = ATTENDANCE.get(student_id)
    if not row:
        return {"error": "Attendance not found"}
    return {**row, "percentage": round(row["attended"] / row["total"] * 100, 2)}


@mcp.resource("college://attendance-policy")
def attendance_policy() -> str:
    """The sample college attendance policy."""
    return "The sample policy requires 75% attendance. Verify the official college handbook before relying on this example."


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
