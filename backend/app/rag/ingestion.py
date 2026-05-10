import json
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from app.config import settings
from app.rag.embeddings import embeddings

client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)

COLLECTION_NAME = "metadata"


def create_collection():
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=settings.OLLAMA_EMBEDDING_DIMENSIONS,
            distance=Distance.COSINE,
        )
    )


def ingest_metadata(file_path: str):
    metadata_path = Path(file_path)
    if not metadata_path.exists():
        raise FileNotFoundError(f"Metadata file not found: {metadata_path}")

    with open(file_path, "r") as f:
        data = json.load(f)

    points = []

    for idx, item in enumerate(data):
        text = json.dumps(item)
        vector = embeddings.embed_query(text)

        points.append(
            PointStruct(
                id=idx,
                vector=vector,
                payload={"text": text}
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )


def ensure_metadata_collection():
    if collection_has_expected_vector_size():
        return

    create_collection()
    ingest_metadata(settings.METADATA_FILE)


def collection_has_expected_vector_size():
    if not client.collection_exists(collection_name=COLLECTION_NAME):
        return False

    collection = client.get_collection(collection_name=COLLECTION_NAME)
    if not collection.points_count:
        return False

    vectors_config = collection.config.params.vectors
    vector_size = getattr(vectors_config, "size", None)

    if vector_size is None and isinstance(vectors_config, dict):
        vector_size = next(iter(vectors_config.values())).size

    return vector_size == settings.OLLAMA_EMBEDDING_DIMENSIONS
