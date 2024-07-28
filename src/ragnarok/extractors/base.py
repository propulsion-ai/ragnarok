from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel

class ExtractorConfig(BaseModel):
    """Base configuration for extractors."""
    pass

class ExtractorOutput(BaseModel):
    """
    Standard output format for extractors.
    """
    text: str
    metadata: Dict[str, Any] = {}

class BaseExtractor(ABC):
    def __init__(self, config: Optional[ExtractorConfig] = None):
        self.config = config or ExtractorConfig()

    @abstractmethod
    def extract(self, source: Any) -> ExtractorOutput:
        """
        Extract text and metadata from the given source.

        Args:
            source (Any): The source to extract from. This could be a file path, 
                          URL, or any other identifier for the source.

        Returns:
            ExtractorOutput: An object containing the extracted text and metadata.
        """
        pass

    @classmethod
    @abstractmethod
    def from_config(cls, config: ExtractorConfig) -> 'BaseExtractor':
        """
        Create an extractor instance from a configuration.

        Args:
            config (ExtractorConfig): The configuration for the extractor.

        Returns:
            BaseExtractor: An instance of the extractor.
        """
        pass