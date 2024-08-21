

import time
from typing import Any, Dict, List, Optional, Union
import uuid
from ..config import VectorStoreConfig
from ..embedders import EmbeddingOutput
from pinecone import Pinecone, PineconeException, PodSpec, ServerlessSpec

from ..logger import RAGnarokLogger
from .base import BaseVectorStore, VectorStoreOutput


class PineconeVectorStore(BaseVectorStore):

    _sleep_duration: int = 1
    _valid_metadata_types = (str, int, bool, List[str])

    def __init__(self, config: dict) -> None:
        self.config = config
        self.logger = RAGnarokLogger.get_logger()
        self.credentials = config.get("credentials", {})

        api_key = self.credentials.get("api_key")
        host = self.credentials.get("host")
        proxy_url = self.credentials.get("proxy_url")
        ssl_verify = self.credentials.get("ssl_verify", False)

        # Additional kwargs for Pinecone Client
        extra_kwargs = {
            k: v
            for k, v in self.credentials.items()
            if k
            not in [
                "api_key",
                "host",
                "proxy_url",
            ]
        }

        self.client = Pinecone(
            api_key=api_key,
            host=host,
            proxy_url=proxy_url,
            ssl_verify=ssl_verify,
            **extra_kwargs,
        )

        self.namespace = config.get("namespace", "default-namespace")
        self.collection_name = config.get("collection_name", "demo-collection")
        self.initialize_collection()

    def initialize_collection(self) -> None:
        try:
            self.client.delete_index(self.collection_name)
            time.sleep(self._sleep_duration)
        
        except PineconeException as e:
            self.logger.error(e)

        self.client.create_index(
            name=self.collection_name,
            dimension=self.config.get("dimension", 1536),
            metric=self.config.get("metric", "cosine"),
            deletion_protection=self.config.get("deletion_protection", "disabled"),
            spec=self._initialize_index_spec(self.config.get("spec", {}))
        )

        while not self.client.describe_index(self.collection_name).index.status["ready"]:
            self.logger.info("Initializing Pinecone index...")
            time.sleep(self._sleep_duration)

        self.index = self.client.Index(
            name=self.collection_name,
        )
    
    def insert(self, embeddings: List[EmbeddingOutput]) -> List[VectorStoreOutput]:
        result = []
        try:
            vectors = []
            for embedding in embeddings:
                self._filter_metadata(embedding.metadata)
                embedding.metadata["text"] = embedding.text
                # Retrieve id, and assign new id if it does not already exist
                if embedding.metadata.get("id"):
                    vector_id = embedding.metadata["id"]
                else:
                    vector_id = str(uuid.uuid4())
                    embedding.metadata["id"] = vector_id

                vectors.append(
                    (vector_id, embedding.vector, embedding.metadata)
                )
            res = self.index.upsert(
                vectors=vectors,
                namespace=self.namespace,
            )
            if res.get("upserted_count") != len(vectors):
                result = self._format_vector_store_output(
                    embeddings,
                    "Pinecone did not insert the correct number of vectors",
                )
            result = self._format_vector_store_output(embeddings)

        except PineconeException as e:
            self.logger.error(e)
            return self._format_vector_store_output(embeddings, str(e))
        
        return result
    
    def search(self, query_vector: List[float], k: int = 5) -> List[EmbeddingOutput]:
        result = []
        try:
            query_response = self.index.query(
                namespace=self.namespace,
                vector=query_vector,
                top_k=k,
                include_values=True,
                include_metadata=True,
            )
            result = [
                EmbeddingOutput(
                    vector=query_match.get("values", []),
                    text=query_match.get("metadata", {}).get("text", ""),
                    metadata=query_match.get("metadata", {})
                )
                for query_match in query_response.get("matches", [])
            ]

        except PineconeException as e:
            self.logger.error(e)
            return []
        
        return result
    
    def delete(self, ids: List[str]) -> None:
        try:
            self.index.delete(
                ids=ids,
                namespace=self.collection_name,
            )

        except PineconeException as e:
            self.logger.error(e)
    
    @classmethod
    def from_config(cls, config: dict) -> "PineconeVectorStore":
        return cls(config)
    
    def _filter_metadata(self, metadata: Dict[str, Any]) -> None:
        # Casting the items() to a list creates a copy, preventing runtime errors
        for key, value in list(metadata.items()):
            if value is None or not isinstance(value, self._valid_metadata_types):
                del metadata[key]
    
    def _initialize_index_spec(self, spec: dict) -> Union[PodSpec, ServerlessSpec]:
        spec_type = spec.get("type", "pod")
        if spec_type == "serverless":
            return ServerlessSpec(
                cloud=spec.get("cloud", "aws"),
                region=spec.get("region", "us-east-1"),
            )
        
        elif spec_type == "pod":
            return PodSpec(
                environment=spec.get("environment", "us-east1-gcp"),
                pod_type=spec.get("pod_type", "p1.x1")
            )
                
        raise ValueError(f"Invalid spec type: {spec_type}")
    
    def _format_vector_store_output(
        self, 
        embeddings: List[EmbeddingOutput], 
        error: Optional[str] = None,
    ) -> List[VectorStoreOutput]:
        status = "success"
        if error:
            status = "error"
        return [
            VectorStoreOutput(
                text=embedding.text,
                vector=embedding.vector,
                metadata=embedding.metadata,
                id=embedding.metadata.get("id", str(uuid.uuid4())),
                status=status,
                error=error
            )
            for embedding in embeddings
        ]
