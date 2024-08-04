from abc import ABC, abstractmethod
from typing import Any, Dict

from ..utils.serializable import JSONSerializable


class ExtractorOutput(JSONSerializable):
    """
    Standard output format for extractors.
    """

    def __init__(self, text: str, metadata: Dict[str, Any]):
        self.text = text
        self.metadata = metadata


class BaseExtractor(ABC):
    def __init__(self, config: dict = None):
        self.config = config

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
    def from_config(cls, config: dict) -> "BaseExtractor":
        """
        Create an extractor instance from a configuration.

        Args:
            config (ExtractorConfig): The configuration for the extractor.

        Returns:
            BaseExtractor: An instance of the extractor.
        """
        pass
