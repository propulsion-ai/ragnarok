from .base import BaseEmbedder, EmbeddingOutput

def get_embedder(embedder_type: str, config: dict) -> BaseEmbedder:
    if embedder_type == "openai":
        from .openai_embedder import OpenAIEmbedder
        return OpenAIEmbedder.from_config(config)
    # elif embedder_type == "sentence_transformers":
    #     from .sentence_transformer_embedder import SentenceTransformerEmbedder
    #     return SentenceTransformerEmbedder.from_config(config)
    # elif embedder_type == "ollama":
    #     from .ollama_embedder import OllamaEmbedder
    #     return OllamaEmbedder.from_config(config)
    else:
        raise ValueError(f"Unknown embedder type: {embedder_type}")

__all__ = ["BaseEmbedder", "get_embedder", "EmbeddingOutput"]