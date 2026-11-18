from langchain.agents import create_agent
from langchain.tools import tool
from langchain_mcp_adapters.client import MultiServerMCPClient
from app.core.config import settings
from app.core.llm import build_chat_model
from app.services.rag_service import RAGService


class CollegeAssistant:
    def __init__(self) -> None:
        self.mcp_client = MultiServerMCPClient({
            "college": {"transport": "http", "url": settings.mcp_server_url}
        })
        self.rag = RAGService()
        self.agent = None

    async def initialize(self) -> None:
        mcp_tools = await self.mcp_client.get_tools()
        rag_service = self.rag

        @tool
        def search_college_policy(question: str) -> str:
            """Search official college policy documents for attendance, fees, library or examination rules."""
            result = rag_service.ask(question)
            return f"Answer: {result['answer']} | Sources: {', '.join(result['sources'])}"

        self.agent = create_agent(
            model=build_chat_model(),
            tools=[*mcp_tools, search_college_policy],
            system_prompt=(
                "You are a college management assistant. Use MCP tools for student-specific "
                "records and the policy search tool for college rules. Never invent database "
                "facts. Clearly distinguish sample policy text from official decisions. "
                "Do not infer a student's identity from a question; this learning project has "
                "no authentication and must not be used with real student data."
            ),
        )

    async def ask(self, question: str) -> str:
        if self.agent is None:
            raise RuntimeError("Assistant has not been initialized")
        result = await self.agent.ainvoke({"messages": [{"role": "user", "content": question}]})
        return result["messages"][-1].content
