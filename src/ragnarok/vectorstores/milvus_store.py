from typing import List, Dict, Any
from pymilvus import MilvusClient
from ..config import VectorStoreConfig

class MilvusVectorStore:
    def __init__(self, config: VectorStoreConfig):
        self.config = config
        self.milvus_config = config.milvus_config or {}
        
        # Determine if it's a URL or file-based connection
        connection_type = self.config.credentials.get("connection_type", "file")
        
        if connection_type == "url":
            # URL-based connection
            uri = self.config.credentials.get("uri", "http://localhost:19530")
            user = self.config.credentials.get("user", "")
            password = self.config.credentials.get("password", "")
            db_name = self.config.credentials.get("db_name", "")
            token = self.config.credentials.get("token", "")
            timeout = self.config.credentials.get("timeout")
            
            # Additional kwargs for MilvusClient
            extra_kwargs = {k: v for k, v in self.config.credentials.items() 
                            if k not in ["uri", "user", "password", "db_name", "token", "timeout", "connection_type"]}
            
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
            file_path = self.config.credentials.get("file_path", "milvus_demo.db")
            
            # Initialize MilvusClient with file-based parameter
            self.client = MilvusClient(file_path)
        
        self.collection_name = config.collection_name

    def initialize_collection(self):
        if self.client.has_collection(collection_name=self.collection_name):
            self.client.drop_collection(collection_name=self.collection_name)
        
        self.client.create_collection(
            collection_name=self.collection_name,
            dimension=self.milvus_config.get("dimension", 768),
        )

    def insert(self, vectors: List[List[float]], texts: List[str], metadata: List[Dict[str, Any]] = None):
        if metadata is None:
            metadata = [{}] * len(vectors)
        
        data = [
            {"id": i, "vector": vectors[i], "text": texts[i], **metadata[i]}
            for i in range(len(vectors))
        ]
        
        res = self.client.insert(collection_name=self.collection_name, data=data)
        return res

    @classmethod
    def from_config(cls, config: VectorStoreConfig) -> 'MilvusVectorStore':
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