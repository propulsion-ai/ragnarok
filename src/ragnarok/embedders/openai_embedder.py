from enum import Enum
from typing import List
from .base import BaseEmbedder
from openai import OpenAI

class ModelEnum(Enum):
    text_embedding_3_small = "text-embedding-3-small"
    text_embedding_3_large = "text-embedding-3-large"
    text_embedding_ada_002 = "text-embedding-ada-002"

class OpenAIEmbedder(BaseEmbedder):
    def __init__(self, config: dict):
        super().__init__(config)
        self.client = OpenAI(api_key=config["api_key"])
        self.model = ModelEnum(config["model"])

    def embed(self, input_text: str) -> List[float]:
        response = self.client.embeddings.create(
            input=input_text,
            model=self.model.value
        )
        return response.data[0].embedding

    @classmethod
    def from_config(cls, config: dict) -> 'OpenAIEmbedder':
        return cls(config)

# Example usage
# config = EmbedderConfig(
#     embedder_type="openai",
#     embedder_model="text-embedding-3-small",
#     api_key="your-api-key-here",
#     openai_config={}  # Add any OpenAI-specific config here if needed
# )
# embedder = OpenAIEmbedder.from_config(config)
# vector = embedder.embed("Your text string goes here")
# print(vector)