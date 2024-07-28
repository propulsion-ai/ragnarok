from .base import BaseChunker, ChunkerConfig
from typing import List

class FixedSizeChunkerConfig(ChunkerConfig):
    chunk_size: int
    overlap: int

class FixedSizeChunker(BaseChunker):
    def __init__(self, config: FixedSizeChunkerConfig):
        super().__init__(config)

    def chunk(self, text: str) -> List[str]:
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.config.chunk_size
            chunks.append(text[start:end])
            start = end - self.config.overlap
        return chunks