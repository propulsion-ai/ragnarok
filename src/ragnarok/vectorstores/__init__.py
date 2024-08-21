from .base import BaseVectorStore


def get_vectorstore(store_type: str, config: dict) -> BaseVectorStore:
    if store_type == "milvus":
        from .milvus_store import MilvusVectorStore
        return MilvusVectorStore.from_config(config)
    elif store_type == "pinecone":
        from .pinecone_store import PineconeVectorStore
        return PineconeVectorStore.from_config(config)
    # elif store_type == "weaviate":
    #     from .weaviate import WeaviateVectorStore
    #     return WeaviateVectorStore.from_config(config)
    # elif store_type == "qdrant":
    #     from .qdrant import QdrantVectorStore
    #     return QdrantVectorStore.from_config(config)
    # elif store_type == "pgvector":
    #     from .pgvector import PGVectorStore
    #     return PGVectorStore.from_config(config)
    else:
        raise ValueError(f"Unknown vector store type: {store_type}")


__all__ = ["BaseVectorStore", "get_vectorstore"]
