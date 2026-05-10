from langchain_ollama import OllamaEmbeddings
from app.config import settings

embeddings = OllamaEmbeddings(
    base_url=settings.OLLAMA_HOST,
    model=settings.OLLAMA_EMBEDDING_MODEL,
)
