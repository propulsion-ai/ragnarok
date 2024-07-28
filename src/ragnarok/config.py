from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from typing import Optional, Callable, Union, List

class ChunkerConfig(BaseModel):
    chunker_type: str
    config: dict

class EmbedderConfig(BaseModel):
    model_url: str
    api_key: Optional[str] = None

class VectorStoreConfig(BaseModel):
    store_type: str
    credentials: dict
    collection_name: str

class RAGnarokConfig(BaseModel):
    chunker: Union[ChunkerConfig, Callable[[str], List[str]]] = Field(
        default_factory=lambda: ChunkerConfig(chunker_type="fixed_size", config={"chunk_size": 1000, "overlap": 200})
    )
    embedder: EmbedderConfig
    vectorstore: VectorStoreConfig

class EmbeddingConfig(BaseModel):
    vector: list[float]
    text: str
    metadata: Optional[dict] = None