<div align="center">
 <img src="assets/logo_dark.svg#gh-light-mode-only" width="400px">
 <img src="assets/logo_light.svg#gh-dark-mode-only" width="400px">
</div>

<p align="center">
  <a href="https://twitter.com/propulsion_ai">
    <img src="https://img.shields.io/badge/twitter-black?logo=x"/>
  </a>
  <a href="https://www.linkedin.com/company/propulsionhq">
    <img src="https://img.shields.io/badge/linkedin-blue?logo=linkedin"/>
  </a>
  <a href="https://discord.gg/J4RF7phwYN">
  <img src="https://img.shields.io/badge/Discord-7289DA?&logo=discord&logoColor=white"/>
  </a>
</p>


RAGnarok is a powerful and flexible tool for document processing and information retrieval. It allows users to chunk documents, embed chunks using state-of-the-art models, and store embeddings in a vector store for efficient retrieval. This ReadMe provides basic instructions for configuring and using RAGnarok in your projects.

## Installation
First, ensure you have RAGnarok installed. You can install it using pip:

```bash
pip install ragnarok
```

## Configuration
To use RAGnarok, you need to configure it with the appropriate settings for chunking, embedding, and vector storage. Below is an example of how to set up and initialize RAGnarok.

## Basic Usage

### Step 1: Import RAGnarok and Configurations

```python
from ragnarok import RAGnarok
from ragnarok.config import RAGnarokConfig, EmbedderConfig, VectorStoreConfig
```

### Step 2: Define a Custom Chunker (Optional)
If you have a custom logic for chunking your documents, you can define your custom chunker function.

```python
def my_custom_chunker(text: str) -> List[str]:
    # Custom chunking logic here
    return chunks
```

### Step 3: Configure RAGnarok
Set up the configuration with your preferred settings. This includes specifying the chunker, embedder, and vector store configurations.

```python
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
```

### Step 4: Initialize RAGnarok
Create an instance of RAGnarok with the configuration.

```python
rag = RAGnarok(config)
```

### Step 5: Process Documents
Use the `process` method to chunk, embed, and store your document.

```python
rag.process("document.pdf")
```

## Example
Here is a complete example of using RAGnarok:

```python
from ragnarok import RAGnarok
from ragnarok.config import RAGnarokConfig, EmbedderConfig, VectorStoreConfig

def my_custom_chunker(text: str) -> List[str]:
    # Custom chunking logic here
    return chunks

# chunker=ChunkerConfig(chunker_type="fixed_size", config={"chunk_size": 1000, "overlap": 100}),

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

rag = RAGnarok(config)
rag.process("document.pdf")
```

## Configuration Details

### `RAGnarokConfig`
- `chunker`: Function for custom chunking logic. Optional.
- `embedder`: Configuration for the embedding model.
  - `model_url`: URL or path to the embedding model.
  - `api_key`: API key for accessing the embedding model, if required.
- `vectorstore`: Configuration for the vector store.
  - `store_type`: Type of vector store (e.g., "milvus").
  - `credentials`: Credentials for connecting to the vector store.
  - `collection_name`: Name of the collection in the vector store.

## Additional Information
For more details, refer to the official documentation or contact support.

## License
RAGnarok is released under the MIT License.

---

Feel free to modify the configurations and functions to fit your specific needs. Happy processing!
