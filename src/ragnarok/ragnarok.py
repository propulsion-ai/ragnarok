from typing import List, Optional
from .config import RAGnarokConfig, ChunkConfig, EmbeddingConfig
from .chunkers import smart_chunker
from .embedders import initialize_embedder
from .vectorstores import initialize_vectorstore

class RAGnarok:
    def __init__(self, config: RAGnarokConfig):
        self.config = config
        self.chunker = config.chunker or smart_chunker
        self.embedder = initialize_embedder(config.embedder)
        self.vectorstore = initialize_vectorstore(config.vectorstore)

    def extract(self, source: str) -> str:
        # Implementation for extraction
        pass

    def chunk(self, text: str) -> List[ChunkConfig]:
        return [ChunkConfig(text=chunk) for chunk in self.chunker(text)]

    def embed(self, chunks: List[ChunkConfig]) -> List[EmbeddingConfig]:
        embeddings = self.embedder.embed([chunk.text for chunk in chunks])
        return [
            EmbeddingConfig(vector=embedding, text=chunk.text, metadata=chunk.metadata)
            for embedding, chunk in zip(embeddings, chunks)
        ]

    def upload(self, embeddings: List[EmbeddingConfig]) -> None:
        self.vectorstore.upload(embeddings)

    def process(self, source: str) -> None:
        text = self.extract(source)
        chunks = self.chunk(text)
        embeddings = self.embed(chunks)
        self.upload(embeddings)