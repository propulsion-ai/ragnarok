import os
from typing import List, Optional, Tuple, Dict, Any, Callable
from .config import RAGnarokConfig, EmbeddingConfig
from .chunkers import get_chunker, ChunkOutput
from .embedders import get_embedder
from .vectorstores import initialize_vectorstore
from .extractors import get_extractor, ExtractorOutput

class RAGnarok:
    def __init__(self, config: RAGnarokConfig):
        self.config = config

        if isinstance(config.chunker, Callable):
            self.chunker = config.chunker
        else:
            self.chunker = get_chunker(config.chunker.chunker_type, config.chunker.config)

        self.embedder = get_embedder(config.embedder)
        self.vectorstore = initialize_vectorstore(config.vectorstore)

    def extract(self, source: str) -> ExtractorOutput:
        file_extension = os.path.splitext(source)[1]
        extractor = get_extractor(file_extension)
        return extractor.extract(source)

    def chunk(self, text: str, metadata: Dict[str, Any]) -> List[ChunkOutput]:
        chunks = self.chunker(text)
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
        chunks = self.chunk(extracted.text, extracted.metadata)
        embeddings = self.embed(chunks)
        self.upload(embeddings)