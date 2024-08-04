from abc import ABC, abstractmethod
from typing import Any, Dict, List

from pydantic import BaseModel

from ..utils.serializable import JSONSerializable


class ChunkerConfig(BaseModel):
    pass


class ChunkOutput(JSONSerializable):
    def __init__(self, text: str, metadata: Dict[str, Any]):
        self.text = text
        self.metadata = metadata


class BaseChunker(ABC):
    def __init__(self, config: ChunkerConfig):
        self.config = config

    @abstractmethod
    def chunk(self, text: str) -> List[str]:
        pass
