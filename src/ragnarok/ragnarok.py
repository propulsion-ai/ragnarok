from typing import Any, Callable, Dict, List

from .chunkers import ChunkOutput, get_chunker
from .config import CrawlerConfig, RAGnarokConfig
from .crawlers import get_crawler
from .embedders import EmbeddingOutput, get_embedder
from .extractors import ExtractorOutput, get_extractor
from .logger import RAGnarokLogger
from .utils import get_source_type
from .vectorstores import get_vectorstore


class RAGnarok:
    def __init__(self, config: RAGnarokConfig):
        self.config = config

        # Set up logging
        RAGnarokLogger.setup_logging(level=config.log_level, file_path=config.log_file)
        self.logger = RAGnarokLogger.get_logger()

        if isinstance(config.chunker, Callable):
            self.chunker = config.chunker
        elif config.chunker is None:
            self.chunker = None
        else:
            self.chunker = get_chunker(
                config.chunker.chunker_type, config.chunker.config
            )

        self.embedder = get_embedder(
            config.embedder.embedder_type, config.embedder.config
        )
        self.vectorstore = get_vectorstore(
            config.vectorstore.store_type, config.vectorstore.config
        )
        self.crawler = None
        if config.crawler:
            self.crawler = get_crawler(config.crawler.type, config.crawler.config)

    def extract(self, source: str, **kwargs) -> ExtractorOutput:
        source_type = get_source_type(source)
        self.logger.info(f"Extracting {source}: {source_type} ...")

        extractor = get_extractor(source_type)

        if source_type == "url":
            if not self.crawler:
                self.logger.warning(
                    "No crawler configured. Proceeding with default crawler..."
                )
                default_config = CrawlerConfig()
                self.crawler = get_crawler(default_config.type, default_config.config)
            return extractor.extract(source, crawler=self.crawler,**kwargs)
        else:
            return extractor.extract(source, **kwargs)

    def chunk(self, text: str, metadata: Dict[str, Any]) -> List[ChunkOutput]:
        if isinstance(self.chunker, Callable):
            chunks = self.chunker(text)
        elif self.chunker is None:
            chunks = [text]
        else:
            chunks = self.chunker.chunk(text)
        return [ChunkOutput(text=chunk, metadata=metadata) for chunk in chunks]

    def embed(self, chunks: List[ChunkOutput]) -> List[EmbeddingOutput]:
        embeddings = []
        for chunk in chunks:
            embedding = self.embedder.embed(chunk.text)
            embeddings.append(embedding)

        return [
            EmbeddingOutput(vector=embedding, text=chunk.text, metadata=chunk.metadata)
            for embedding, chunk in zip(embeddings, chunks)
        ]

    def upload(self, embeddings: List[EmbeddingOutput]) -> None:
        self.vectorstore.upload(embeddings)

    def process(self, source: str) -> None:
        extracted = self.extract(source)
        for item in extracted:
            chunks = self.chunk(item.text, item.metadata)
            embeddings = self.embed(chunks)
            self.upload(embeddings)
