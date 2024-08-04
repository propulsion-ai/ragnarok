from typing import Any
from .base import BaseExtractor, ExtractorOutput
from ..crawlers.base import BaseCrawler

class URLExtractor(BaseExtractor):
    def __init__(self, config: dict):
        super().__init__(config)
        self.depth = config.get("depth", 0)

    def extract(self, source: Any, crawler: BaseCrawler, *args, **kwargs) -> ExtractorOutput:
        if self.depth < 0:
            raise ValueError("Depth must be greater than or equal to 0")
        else:
            return crawler.crawl(source, depth=self.depth)

    @classmethod
    def from_config(cls, config: dict) -> "URLExtractor":
        return cls(config)