"""Lesson 06: embedding + Qdrant similarity search, without an LLM answer."""
import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient, models

load_dotenv()


def main() -> None:
    url, key = os.getenv("QDRANT_URL"), os.getenv("QDRANT_API_KEY")
    if not os.getenv("OPENAI_API_KEY") or not url or not key:
        raise RuntimeError("Set OPENAI_API_KEY, QDRANT_URL and QDRANT_API_KEY")
    embeddings = OpenAIEmbeddings(model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"))
    client = QdrantClient(url=url, api_key=key)
    collection = os.getenv("QDRANT_COLLECTION", "college_vector_lesson")
    # For a clean repeatable lesson, recreate this dedicated practice collection.
    if client.collection_exists(collection):
        client.delete_collection(collection)
    dimension = len(embeddings.embed_query("vector dimension probe"))
    client.create_collection(collection_name=collection, vectors_config=models.VectorParams(size=dimension, distance=models.Distance.COSINE))
    store = QdrantVectorStore(client=client, collection_name=collection, embeddings=embeddings)
    docs = [
        Document(page_content="Students need at least 75 percent attendance for semester examinations.", metadata={"topic": "attendance", "source": "rules.txt"}),
        Document(page_content="Semester examination fees must be paid before the due date.", metadata={"topic": "fees", "source": "rules.txt"}),
        Document(page_content="Library books should be returned on or before the due date.", metadata={"topic": "library", "source": "rules.txt"}),
    ]
    store.add_documents(docs)
    query = "How many classes should I attend to be exam eligible?"
    print("Query:", query)
    for hit in store.similarity_search_with_score(query, k=3):
        doc, score = hit
        print({"score": round(score, 4), "text": doc.page_content, "metadata": doc.metadata})


if __name__ == "__main__":
    main()
