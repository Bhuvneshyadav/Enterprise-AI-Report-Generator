import json
from qdrant_client import QdrantClient
from app.rag.embeddings import embeddings
from app.config import settings
from app.rag.ingestion import COLLECTION_NAME, ensure_metadata_collection

client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)


def retrieve_metadata(query: str):
    ensure_metadata_collection()

    vector = embeddings.embed_query(query)

    if hasattr(client, "search"):
        results = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=vector,
            limit=5,
        )
    else:
        results = client.query_points(
            collection_name=COLLECTION_NAME,
            query=vector,
            limit=5,
        ).points

    metadata = [r.payload["text"] for r in results if r.payload and "text" in r.payload]
    canonical_metadata = load_metadata_file()

    seen = set()
    merged_metadata = []

    for item in metadata + canonical_metadata:
        if item not in seen:
            seen.add(item)
            merged_metadata.append(item)

    return merged_metadata


def load_metadata_file():
    with open(settings.METADATA_FILE, "r") as metadata_file:
        return [json.dumps(item) for item in json.load(metadata_file)]
