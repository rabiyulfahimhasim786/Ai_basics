from pathlib import Path
from app.services.vector_service import ingest_policy_file

if __name__ == "__main__":
    source = Path(__file__).resolve().parents[1] / "app" / "data" / "college_rules.txt"
    count = ingest_policy_file(source)
    print(f"Upserted {count} policy chunks into Qdrant.")
