import os
import pytest
from dotenv import load_dotenv, find_dotenv
from typing import Any
from src.ragnarok.ragnarok import RAGnarok
from src.ragnarok.config import RAGnarokConfig, EmbedderConfig, VectorStoreConfig
from .common import simple_chunker

load_dotenv(find_dotenv())

def get_pinecone_test_configs() -> dict[str, Any]:
    pinecone_api_key = os.getenv("PINECONE_API_KEY")

    if pinecone_api_key is None:
        raise SystemExit(1)
    
    return [
        {
            "api_key": pinecone_api_key,
            "collection_name": "ragnarok",
            "spec": {
                "type": "serverless",
            }
        },
        {
            "api_key": pinecone_api_key,
            "collection_name": "ragnarok",
            "metric": "cosine",
            "dimension": 1536,
            "spec": {
                "type": "serverless",
            }
        },
    ]


class TestPineconeStore:

    @pytest.mark.parametrize("config", get_pinecone_test_configs())
    def test_pinecone_store(self, config: dict[str, Any]) -> None:
        open_ai_api_key = os.getenv("OPEN_AI_API_KEY")

        if open_ai_api_key is None:
            raise SystemExit(1)
        
        ragnarok_config = RAGnarokConfig(
            chunker=simple_chunker,
            embedder=EmbedderConfig(
                embedder_type="openai",
                config={
                    "model": "text-embedding-3-small",
                    "api_key": open_ai_api_key,
                }
            ),
            vectorstore=VectorStoreConfig(
                store_type="pinecone",
                config=config,
            ),
        )
        rag = RAGnarok(ragnarok_config)
        rag.process("./sample.pdf")