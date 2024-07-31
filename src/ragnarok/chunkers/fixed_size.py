from .base import BaseChunker
from typing import List

class FixedSizeChunker(BaseChunker):
    def __init__(self, config: dict):
        super().__init__(config)
        self.chunk_size = config.get('chunk_size', 1000)
        self.overlap = config.get('overlap', 100)

    def chunk(self, text: str) -> List[str]:
        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + self.chunk_size

            if end >= text_length:
                chunks.append(text[start:])
                break

            # Find the last period or newline within the chunk
            last_period = text.rfind(".", start, end)
            last_newline = text.rfind("\n", start, end)
            split_point = max(last_period, last_newline)

            if split_point == -1 or split_point <= start:
                split_point = (
                    end  # If no suitable split point, just split at chunk_size
                )

            chunks.append(text[start:split_point])
            start = split_point - self.overlap  # Move back by overlap amount

        return chunks
    
    @classmethod
    def from_config(cls, config: dict) -> 'FixedSizeChunker':
        return cls(config)