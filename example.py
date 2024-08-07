import json
from ragnarok import RAGnarok, RAGnarokConfig, ChunkerConfig, EmbedderConfig, VectorStoreConfig, CrawlerConfig

config = RAGnarokConfig(
    chunker=None,
    # chunker=ChunkerConfig(
    #     chunker_type="fixed_size", config={"chunk_size": 1000, "overlap": 100}
    # ),
    # crawler=CrawlerConfig(type="playwright", config={"browser": "firefox", "proxies": proxies}),
    embedder=EmbedderConfig(
        embedder_type="openai",
        config={
            "model":"text-embedding-3-small",
            "api_key":"sk-proj-xVfqZvYl7BGizegROFxQT3BlbkFJZEawMMDbZBNppuLnS8Vn",
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

content = rag.extract("https://developers.facebook.com/docs/", depth=2, save_checkpoint=True)
all_chunks = []

for item in content:
    chunks = rag.chunk(item.text, item.metadata)
    all_chunks.extend(chunks)

chunks_json = json.dumps([chunk.to_dict() for chunk in all_chunks], indent=2)

# save in a jsonl file
with open("output.jsonl", "w") as f:
    for chunk in all_chunks:
        f.write(json.dumps(chunk.to_dict()) + "\n")

# # save in a json file
# with open("output.json", "w") as f:
#     f.write(chunks_json)

# chunks_json = json.dumps([chunk.to_dict() for chunk in chunks], indent=4)
# print(chunks_json)
# print(chunks)

# embeddings = rag.embed(chunks)

# for embedding in embeddings:
#     print(f"Text: {embedding.text}")
#     print(f"Embedding: {embedding.vector[:50]}")
