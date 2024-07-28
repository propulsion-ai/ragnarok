from .base import BaseChunker, ChunkerConfig
from .fixed_size import FixedSizeChunker, FixedSizeChunkerConfig
from .semantic import SemanticChunker, SemanticChunkerConfig
from typing import List

class HybridChunkerConfig(ChunkerConfig):
    fixed_size_config: FixedSizeChunkerConfig
    semantic_config: SemanticChunkerConfig

class HybridChunker(BaseChunker):
    def __init__(self, config: HybridChunkerConfig):
        super().__init__(config)
        self.fixed_size_chunker = FixedSizeChunker(config.fixed_size_config)
        self.semantic_chunker = SemanticChunker(config.semantic_config)

    def chunk(self, text: str) -> List[str]:
        fixed_size_chunks = self.fixed_size_chunker.chunk(text)
        final_chunks = []

        for chunk in fixed_size_chunks:
            semantic_chunks = self.semantic_chunker.chunk(chunk)
            final_chunks.extend(semantic_chunks)

        return final_chunks