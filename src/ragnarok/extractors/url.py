from typing import Any
from .base import BaseExtractor, ExtractorOutput
from ..crawlers.base import BaseCrawler

class URLExtractor(BaseExtractor):
    def __init__(self, config: dict):
        super().__init__(config)

    def extract(self, source: Any, crawler: BaseCrawler, **kwargs) -> ExtractorOutput:
        depth = kwargs.get("depth", 0)
        if depth < 0:
            raise ValueError("Depth must be greater than or equal to 0")
        else:
            return crawler.crawl(source, depth=depth)

    @classmethod
    def from_config(cls, config: dict) -> "URLExtractor":
        return cls(config)