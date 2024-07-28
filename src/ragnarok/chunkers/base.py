from abc import ABC, abstractmethod
from typing import List, Dict, Any
from pydantic import BaseModel, Field

class ChunkerConfig(BaseModel):
    pass

class ChunkOutput(BaseModel):
    text: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class BaseChunker(ABC):
    def __init__(self, config: ChunkerConfig):
        self.config = config

    @abstractmethod
    def chunk(self, text: str) -> List[str]:
        pass