# 03 – Model Context Protocol (MCP)

**Goal:** Publish college functions as MCP tools so compatible AI hosts can discover and call them. MCP is a protocol, not an LLM or agent.

Install `mcp` and run `python server.py`. This lesson uses the Python SDK's `FastMCP` API and Streamable HTTP transport. The default endpoint is `http://127.0.0.1:8001/mcp`.

Try an MCP Inspector/client to list the tools and invoke `student_details` or `attendance_details`.
