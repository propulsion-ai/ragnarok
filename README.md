from ragnarok import RAGnarok
from ragnarok.config import RAGnarokConfig, EmbedderConfig, VectorStoreConfig

# Define custom chunker if needed
def my_custom_chunker(text: str) -> List[str]:
    # Custom chunking logic here
    return chunks

# Configure RAGnarok
config = RAGnarokConfig(
    chunker=my_custom_chunker,  # Optional: Use custom chunker
    embedder=EmbedderConfig(
        model_url="sentence-transformers/all-MiniLM-L6-v2",
        api_key="your_api_key_if_needed"
    ),
    vectorstore=VectorStoreConfig(
        store_type="milvus",
        credentials={"host": "localhost", "port": 19530},
        collection_name="my_collection"
    )
)

# Initialize RAGnarok with the configuration
rag = RAGnarok(config)

# Use RAGnarok
rag.process("document.pdf")