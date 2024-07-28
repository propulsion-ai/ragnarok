from abc import ABC, abstractmethod
from typing import List
from ..config import EmbedderConfig

class BaseEmbedder(ABC):
    def __init__(self, config: EmbedderConfig):
        self.config = config

    @abstractmethod
    def embed(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of texts into a list of vector representations.

        Args:
            texts (List[str]): A list of texts to embed.

        Returns:
            List[List[float]]: A list of vector representations.
        """
        pass

    @classmethod
    @abstractmethod
    def from_config(cls, config: EmbedderConfig) -> 'BaseEmbedder':
        """
        Create an embedder instance from a configuration.

        Args:
            config (EmbedderConfig): The configuration for the embedder.

        Returns:
            BaseEmbedder: An instance of the embedder.
        """
        pass