# from .base import BaseChunker, ChunkerConfig
# from typing import List
# import nltk

# nltk.download('punkt')

# class SemanticChunkerConfig(ChunkerConfig):
#     min_chunk_size: int = 100
#     max_chunk_size: int = 1000

# class SemanticChunker(BaseChunker):
#     def __init__(self, config: SemanticChunkerConfig):
#         super().__init__(config)

#     def chunk(self, text: str) -> List[str]:
#         sentences = nltk.sent_tokenize(text)
#         chunks = []
#         current_chunk = ""

#         for sentence in sentences:
#             if len(current_chunk) + len(sentence) > self.config.max_chunk_size and len(current_chunk) >= self.config.min_chunk_size:
#                 chunks.append(current_chunk.strip())
#                 current_chunk = sentence
#             else:
#                 current_chunk += " " + sentence

#         if current_chunk:
#             chunks.append(current_chunk.strip())

#         return chunks