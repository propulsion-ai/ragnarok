from abc import ABC, abstractmethod
from typing import List, Optional
from ..embedders import EmbeddingOutput
from ..config import VectorStoreConfig

class BaseVectorStore(ABC):
    def __init__(self, config: VectorStoreConfig):
        self.config = config

    @abstractmethod
    def upload(self, embeddings: List[EmbeddingOutput]) -> None:
        """
        Upload a list of embeddings to the vector store.

        Args:
            embeddings (List[EmbeddingOutput]): A list of embeddings to upload.
        """
        pass

    @abstractmethod
    def search(self, query_vector: List[float], k: int = 5) -> List[EmbeddingOutput]:
        """
        Search for the k nearest neighbors of the query vector.

        Args:
            query_vector (List[float]): The query vector to search for.
            k (int): The number of nearest neighbors to return.

        Returns:
            List[EmbeddingOutput]: A list of the k nearest neighbors.
        """
        pass

    @abstractmethod
    def delete(self, ids: List[str]) -> None:
        """
        Delete embeddings from the vector store by their IDs.

        Args:
            ids (List[str]): A list of IDs to delete.
        """
        pass

    @classmethod
    @abstractmethod
    def from_config(cls, config: VectorStoreConfig) -> 'BaseVectorStore':
        """
        Create a vector store instance from a configuration.

        Args:
            config (VectorStoreConfig): The configuration for the vector store.

        Returns:
            BaseVectorStore: An instance of the vector store.
        """
        pass