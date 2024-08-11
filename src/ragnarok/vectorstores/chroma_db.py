import uuid
from typing import Any, Dict, List

import chromadb
from chromadb.config import Settings

from ragnarok.config import VectorStoreConfig

from ..embedders import EmbeddingOutput
from .base import BaseVectorStore, VectorStoreOutput

class ChromaVectorStore(BaseVectorStore):
    def __init__(self, config: dict):
        self.config = config
        self.credentials = config.get("credentials", {})

        # Determine if it's a URL or file-based connection
        connection_type = self.credentials.get("connection_type", "file")

        if connection_type == "url":
            # URL-based connection
            uri = self.credentials.get("uri", "localhost")
            port = self.credentials.get("port", "8000")
            ssl = self.credentials.get("ssl", False)
            headers = self.credentials.get("headers", {})

            # Additional kwargs for client
            extra_kwargs = {
                k: v
                for k, v in self.credentials.items()
                if k
                not in [
                    "uri",
                    "port",
                    "ssl",
                    "headers",
                    "settings",
                    "connection_type",
                ]
            }

            settings = self.credentials.get("settings", Settings(**extra_kwargs))


            self.client = chromadb.HttpClient(
                host=uri,
                port=port,
                ssl=ssl,
                headers=headers,
                settings=settings
            )


        else:
            # File-based connection (default)
            file_path = self.credentials.get("file_path", "milvus_demo.db")
            settings = self.credentials.get("settings", Settings(**extra_kwargs))

            self.client = chromadb.PersistentClient(path=file_path, settings=settings)

        self.collection_name = config.get("collection_name", "demo_collection")

    
    def initialize_collection(self):
        if self.collection_name in self.client.list_collections():
            self.client.drop_collection(collection_name=self.collection_name)

        self.client.create_collection(
            name=self.collection_name
        )
    
    def insert(self, embeddings: List[EmbeddingOutput] = None) -> List[VectorStoreOutput]:
        result = []
        for embedding in embeddings:
            collection = self.client.get_collection(
                name=self.collection_name
            )
            try:
                collection.add(embeddings=embedding)
            except ValueError:
                result.append(
                    VectorStoreOutput(
                        text=embedding.text,
                        metadata=embedding.metadata,
                        vector=embedding.vector,
                        id=embedding.metadata.get("id", str(uuid.uuid4())),
                        status="error",
                        error="Did not provide either embeddings or documents OR The length of ids, embeddings, metadatas, or documents don't match OR Did not provide an embedding function and don't provide embeddings.",
                    )
                )
                continue
            result.append(
                VectorStoreOutput(
                    text=embedding.text,
                    metadata=embedding.metadata,
                    vector=embedding.vector,
                    id=id,
                    status="success",
                )
            )
        
        return result

    def search(self, query_vector: List[float], k: int = 5) -> List[EmbeddingOutput]:
        if query_vector is None:
            raise ValueError("You must provide query_vector")

        collection = self.client.get_collection(name=self.collection_name)
        results = collection.query(
            query_embeddings=query_vector,
            n_results=k,
        )
        return results
    
    def delete(self, ids: List[str]) -> None:
        collection = self.client.get_collection(name=self.collection_name)
        collection.delete(ids=ids)

    @classmethod
    def from_config(cls, config: dict) -> "ChromaVectorStore":
        return cls(config)
        

