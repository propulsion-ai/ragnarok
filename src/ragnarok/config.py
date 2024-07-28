from pydantic import BaseModel, Field
from typing import Optional, Callable

class EmbedderConfig(BaseModel):
    model_url: str
    api_key: Optional[str] = None

class VectorStoreConfig(BaseModel):
    store_type: str
    credentials: dict
    collection_name: str

class RAGnarokConfig(BaseModel):
    chunker: Optional[Callable] = None
    embedder: EmbedderConfig
    vectorstore: VectorStoreConfig

class ChunkConfig(BaseModel):
    text: str
    metadata: Optional[dict] = None

class EmbeddingConfig(BaseModel):
    vector: list[float]
    text: str
    metadata: Optional[dict] = None