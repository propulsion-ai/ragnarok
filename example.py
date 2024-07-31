from ragnarok import RAGnarok, RAGnarokConfig, ChunkerConfig, EmbedderConfig, VectorStoreConfig

config = RAGnarokConfig(
    chunker=ChunkerConfig(
        chunker_type="fixed_size", config={"chunk_size": 1000, "overlap": 100}
    ),
    embedder=EmbedderConfig(
        embedder_type="openai",
        config={
            "model":"text-embedding-3-small",
            "api_key":"your_api_key_if_needed",
        }
    ),
    vectorstore=VectorStoreConfig(
        store_type="milvus",
        config={
            "collection_name": "my_collection",
            "credentials": {
                "host": "localhost",
                "port": 19530,
            }
        }
    )
)

rag = RAGnarok(config)

content = rag.extract("sample.pdf")
for item in content:
    chunks = rag.chunk(item.text, item.metadata)

print(chunks)
