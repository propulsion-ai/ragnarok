import os
from typing import List, Optional, Tuple, Dict, Any, Callable
from .config import RAGnarokConfig, EmbeddingConfig
from .chunkers import get_chunker, ChunkOutput
from .embedders import get_embedder
from .vectorstores import get_vectorstore
from .extractors import get_extractor, ExtractorOutput
from .utils import get_source_type

class RAGnarok:
    def __init__(self, config: RAGnarokConfig):
        self.config = config

        if isinstance(config.chunker, Callable):
            self.chunker = config.chunker
        else:
            self.chunker = get_chunker(config.chunker.chunker_type, config.chunker.config)

        self.embedder = get_embedder(config.embedder.embedder_type, config.embedder.config)
        self.vectorstore = get_vectorstore(config.vectorstore.store_type, config.vectorstore.config)

    def extract(self, source: str) -> ExtractorOutput:
        extractor = get_extractor(get_source_type(source))
        return extractor.extract(source)

    def chunk(self, text: str, metadata: Dict[str, Any]) -> List[ChunkOutput]:
        if isinstance(self.chunker, Callable):
            chunks = self.chunker(text)
        else:
            chunks = self.chunker.chunk(text)
        return [ChunkOutput(text=chunk, metadata=metadata) for chunk in chunks]

    def embed(self, chunks: List[ChunkOutput]) -> List[EmbeddingConfig]:
        embeddings = self.embedder.embed([chunk.text for chunk in chunks])
        return [
            EmbeddingConfig(vector=embedding, text=chunk.text, metadata=chunk.metadata)
            for embedding, chunk in zip(embeddings, chunks)
        ]

    def upload(self, embeddings: List[EmbeddingConfig]) -> None:
        self.vectorstore.upload(embeddings)

    def process(self, source: str) -> None:
        extracted = self.extract(source)
        for item in extracted:
            chunks = self.chunk(item.text, item.metadata)
            embeddings = self.embed(chunks)
            self.upload(embeddings)