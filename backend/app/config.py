from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OLLAMA_HOST: str = "http://host.docker.internal:11434"
    OLLAMA_MODEL: str = "llama3.1:8b"
    OLLAMA_EMBEDDING_MODEL: str = "nomic-embed-text"
    OLLAMA_EMBEDDING_DIMENSIONS: int = 768
    MYSQL_URL: str
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    METADATA_FILE: str = "/metadata/sales_schema.json"

    class Config:
        env_file = ".env"

settings = Settings()
