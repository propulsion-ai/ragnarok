from .base import BaseChunker, ChunkOutput
from .fixed_size import FixedSizeChunker, FixedSizeChunkerConfig
# from .semantic import SemanticChunker, SemanticChunkerConfig
# from .hybrid import HybridChunker, HybridChunkerConfig

CHUNKER_MAP = {
    'fixed_size': FixedSizeChunker,
    # 'semantic': SemanticChunker,
    # 'hybrid': HybridChunker
}

def get_chunker(chunker_type: str, config: dict) -> BaseChunker:
    """
    Factory function to get the appropriate chunker based on the chunker type.
    
    Args:
        chunker_type (str): The type of chunker ('fixed_size', 'semantic', or 'hybrid')
        config (ChunkerConfig): The configuration for the chunker
    
    Returns:
        BaseChunker: An instance of the appropriate chunker
    
    Raises:
        ValueError: If no chunker is available for the given type
    """
    chunker_class = CHUNKER_MAP.get(chunker_type.lower())
    if chunker_class is None:
        raise ValueError(f"No chunker available for type: {chunker_type}")
    
    return chunker_class(config)

__all__ = [
    'BaseChunker',
    # 'ChunkerConfig',
    'ChunkOutput',
    'FixedSizeChunker',
    'FixedSizeChunkerConfig',
    # 'SemanticChunker',
    # 'SemanticChunkerConfig',
    # 'HybridChunker',
    # 'HybridChunkerConfig',
    'get_chunker',
]