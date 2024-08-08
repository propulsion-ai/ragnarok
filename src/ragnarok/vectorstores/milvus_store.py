import uuid
from typing import Any, Dict, List

from pymilvus import MilvusClient

from ..embedders import EmbeddingOutput
from .base import BaseVectorStore, VectorStoreOutput


class MilvusVectorStore(BaseVectorStore):
    def __init__(self, config: dict):
        self.config = config
        self.credentials = config.get("credentials", {})

        # Determine if it's a URL or file-based connection
        connection_type = self.credentials.get("connection_type", "file")

        if connection_type == "url":
            # URL-based connection
            uri = self.credentials.get("uri", "http://localhost:19530")
            user = self.credentials.get("user", "")
            password = self.credentials.get("password", "")
            db_name = self.credentials.get("db_name", "")
            token = self.credentials.get("token", "")
            timeout = self.credentials.get("timeout")

            # Additional kwargs for MilvusClient
            extra_kwargs = {
                k: v
                for k, v in self.credentials.items()
                if k
                not in [
                    "uri",
                    "user",
                    "password",
                    "db_name",
                    "token",
                    "timeout",
                    "connection_type",
                ]
            }

            # Initialize MilvusClient with URL-based parameters
            self.client = MilvusClient(
                uri=uri,
                user=user,
                password=password,
                db_name=db_name,
                token=token,
                timeout=timeout,
                **extra_kwargs
            )
        else:
            # File-based connection (default)
            file_path = self.credentials.get("file_path", "milvus_demo.db")

            # Initialize MilvusClient with file-based parameter
            self.client = MilvusClient(file_path)

        self.collection_name = config.get("collection_name", "demo_collection")

    def initialize_collection(self):
        if self.client.has_collection(collection_name=self.collection_name):
            self.client.drop_collection(collection_name=self.collection_name)

        self.client.create_collection(
            collection_name=self.collection_name,
            dimension=self.config.get("dimension", 768),
        )

    def insert(self, embeddings: List[EmbeddingOutput] = None) -> List[VectorStoreOutput]:
        result = []
        try:
            for embedding in embeddings:
                res = self.client.insert(
                    collection_name=self.collection_name,
                    data=[
                        {
                            "vector": embedding.vector,
                            "metadata": embedding.metadata,
                        }
                    ],
                )

                if res["status"]["code"] != 0:
                    result.append(
                        VectorStoreOutput(
                            text=embedding.text,
                            metadata=embedding.metadata,
                            vector=embedding.vector,
                            id=embedding.metadata.get("id", str(uuid.uuid4())),
                            status="error",
                            error=res["status"]["message"],
                        )
                    )
                    continue
                elif len(res["ids"]) == 0:
                    result.append(
                        VectorStoreOutput(
                            text=embedding.text,
                            metadata=embedding.metadata,
                            vector=embedding.vector,
                            id=embedding.metadata.get("id", str(uuid.uuid4())),
                            status="error",
                            error="No ID returned by Milvus",
                        )
                    )
                    continue
                else:
                    id = res["ids"][0]
                    result.append(
                        VectorStoreOutput(
                            text=embedding.text,
                            metadata=embedding.metadata,
                            vector=embedding.vector,
                            id=id,
                            status="success",
                        )
                    )
        except Exception as e:
            return [
                VectorStoreOutput(
                    text=embedding.text,
                    metadata=embedding.metadata,
                    vector=embedding.vector,
                    id=embedding.metadata.get("id", str(uuid.uuid4())),
                    status="error",
                    error=str(e),
                )
                for embedding in embeddings
            ]
        return result

    @classmethod
    def from_config(cls, config: dict) -> "MilvusVectorStore":
        return cls(config)


# Example usage for URL-based connection:
# config_url = VectorStoreConfig(
#     store_type="milvus",
#     credentials={
#         "connection_type": "url",
#         "uri": "http://localhost:19530",
#         "user": "your_username",
#         "password": "your_password",
#         "db_name": "your_db_name",
#         "token": "your_token",
#         "timeout": 30.0,
#         # Any additional kwargs for MilvusClient can be added here
#     },
#     collection_name="demo_collection",
#     milvus_config={
#         "dimension": 768,
#     }
# )

# Example usage for file-based connection (default):
# config_file = VectorStoreConfig(
#     store_type="milvus",
#     credentials={
#         "file_path": "milvus_demo.db",  # Optional, defaults to "milvus_demo.db" if not provided
#     },
#     collection_name="demo_collection",
#     milvus_config={
#         "dimension": 768,
#     }
# )
# import random
# docs = [
#     "Artificial intelligence was founded as an academic discipline in 1956.",
#     "Alan Turing was the first person to conduct substantial research in AI.",
#     "Born in Maida Vale, London, Turing was raised in southern England.",
# ]

# milvus_store = MilvusVectorStore.from_config(config_file)  # or config_url
# milvus_store.initialize_collection()
# vectors = [[random.uniform(-1, 1) for _ in range(768)] for _ in docs]
# data = [
#     {"id": i, "vector": vectors[i], "text": docs[i], "subject": "history"}
#     for i in range(len(vectors))
# ]
# res = milvus_store.insert(vectors, data)
# print(res)
