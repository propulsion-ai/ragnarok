from typing import Any
from .base import BaseExtractor, ExtractorConfig, ExtractorOutput

class URLExtractorConfig(ExtractorConfig):
    extract_metadata: bool = True


class URLExtractor(BaseExtractor):
    def __init__(self, config: URLExtractorConfig):
        super().__init__(config)

    def extract(self, source: Any) -> ExtractorOutput:
        text = ""
        metadata = {}
        return [ExtractorOutput(text=text, metadata=metadata)]

    @classmethod
    def from_config(cls, config: URLExtractorConfig) -> "URLExtractor":
        return cls(config)