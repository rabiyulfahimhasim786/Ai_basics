"""Lesson 05: minimal RAG using Qdrant Cloud."""
import os
from pathlib import Path
from uuid import uuid5, NAMESPACE_URL
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient, models

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


def build_store() -> QdrantVectorStore:
    url, api_key = os.getenv("QDRANT_URL"), os.getenv("QDRANT_API_KEY")
    if not url or not api_key:
        raise RuntimeError("Set QDRANT_URL and QDRANT_API_KEY")
    embeddings = OpenAIEmbeddings(model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"))
    client = QdrantClient(url=url, api_key=api_key)
    collection = os.getenv("QDRANT_COLLECTION", "college_policy_rag")
    size = len(embeddings.embed_query("dimension check"))
    if not client.collection_exists(collection):
        client.create_collection(collection_name=collection, vectors_config=models.VectorParams(size=size, distance=models.Distance.COSINE))
    store = QdrantVectorStore(client=client, collection_name=collection, embeddings=embeddings)
    text = (Path(__file__).parent / "college_rules.txt").read_text(encoding="utf-8")
    chunks = RecursiveCharacterTextSplitter(chunk_size=450, chunk_overlap=60).split_documents([
        Document(page_content=text, metadata={"source": "college_rules.txt"})
    ])
    # Deterministic IDs make this sample ingestion repeatable without duplicating chunks.
    ids = [str(uuid5(NAMESPACE_URL, f"college_rules:{i}:{chunk.page_content}")) for i, chunk in enumerate(chunks)]
    store.add_documents(chunks, ids=ids)
    return store


def main() -> None:
    # Embeddings still use OpenAI; OpenRouter is used for the chat/answer model.
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("Set OPENAI_API_KEY for embeddings")
    store = build_store()
    question = "What attendance percentage is required for semester exams?"
    docs = store.similarity_search(question, k=3)
    context = "\n\n".join(d.page_content for d in docs)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer only from the retrieved policy context. If it does not contain the answer, say you cannot find it. Include the source filename.\nContext:\n{context}"),
        ("human", "{question}"),
    ])
    chain = prompt | build_chat_model()
    print(chain.invoke({"context": context, "question": question}).content)
    print("Retrieved sources:", [d.metadata for d in docs])


if __name__ == "__main__":
    main()
