from pathlib import Path
from uuid import uuid5, NAMESPACE_URL
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient, models
from app.core.config import settings


def get_qdrant_client() -> QdrantClient:
    return QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)


def get_embeddings() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(model=settings.embedding_model)


def ensure_collection(client: QdrantClient) -> None:
    name = settings.qdrant_collection
    if not client.collection_exists(name):
        dimension = len(get_embeddings().embed_query("dimension probe"))
        client.create_collection(collection_name=name, vectors_config=models.VectorParams(size=dimension, distance=models.Distance.COSINE))


def get_vector_store() -> QdrantVectorStore:
    client = get_qdrant_client()
    ensure_collection(client)
    return QdrantVectorStore(client=client, collection_name=settings.qdrant_collection, embeddings=get_embeddings())


def ingest_policy_file(file_path: Path) -> int:
    text = file_path.read_text(encoding="utf-8")
    docs = [Document(page_content=text, metadata={"source": file_path.name, "document_type": "college_policy"})]
    chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80).split_documents(docs)
    store = get_vector_store()
    ids = [str(uuid5(NAMESPACE_URL, f"{file_path.name}:{i}:{chunk.page_content}")) for i, chunk in enumerate(chunks)]
    store.add_documents(chunks, ids=ids)
    return len(chunks)


def search_policy(question: str, k: int = 4) -> list[Document]:
    return get_vector_store().similarity_search(question, k=k)
