from app.rag.ingestion import create_collection, ingest_metadata
from app.config import settings

create_collection()

ingest_metadata(settings.METADATA_FILE)

print("Metadata ingestion completed")
