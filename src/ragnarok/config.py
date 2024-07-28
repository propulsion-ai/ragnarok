from pydantic import BaseModel, Field
from typing import Optional, Callable, Dict, Any

class EmbedderConfig(BaseModel):
    embedder_type: str
    openai_config: Optional[dict] = None

class VectorStoreConfig(BaseModel):
    store_type: str
    credentials: dict
    collection_name: str
    milvus_config: Optional[Dict[str, Any]] = None

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