from typing import Any, Callable, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class ChunkerConfig(BaseModel):
    chunker_type: str
    config: Optional[dict] = None


class EmbedderConfig(BaseModel):
    embedder_type: str
    config: Optional[dict] = None


class VectorStoreConfig(BaseModel):
    store_type: str
    config: Optional[dict] = None


class CrawlerConfig(BaseModel):
    type: str = "playwright"
    config: Optional[Dict[str, Any]] = {"proxies": [], "browser": "firefox"}


class RAGnarokConfig(BaseModel):
    log_level: str = "INFO"
    log_file: Optional[str] = None
    chunker: Optional[Union[ChunkerConfig, Callable[[str], List[str]]]] = Field(
        default=lambda: ChunkerConfig(
            chunker_type="fixed_size", config={"chunk_size": 1000, "overlap": 200}
        )
    )
    crawler: Optional[CrawlerConfig] = None
    embedder: EmbedderConfig
    vectorstore: VectorStoreConfig
