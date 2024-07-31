from .base import BaseExtractor, ExtractorConfig, ExtractorOutput
from .pdf import PDFExtractor
from .url import URLExtractor
# from .text import TextExtractor, TextExtractorConfig
# from .image import ImageExtractor, ImageExtractorConfig
# from .doc import DocExtractor, DocExtractorConfig

# You can create a dictionary mapping file extensions to their respective extractors
EXTRACTOR_MAP = {
    '.pdf': PDFExtractor,
    'url': URLExtractor,
    # '.txt': TextExtractor,
    # '.jpg': ImageExtractor,
    # '.jpeg': ImageExtractor,
    # '.png': ImageExtractor,
    # '.doc': DocExtractor,
    # '.docx': DocExtractor,
}

def get_extractor(source_type: str) -> BaseExtractor:
    """
    Factory function to get the appropriate extractor based on file extension.
    
    Args:
        file_extension (str): The file extension (including the dot)
    
    Returns:
        BaseExtractor: An instance of the appropriate extractor
    
    Raises:
        ValueError: If no extractor is available for the given file extension
    """
    extractor_class = EXTRACTOR_MAP.get(source_type.lower())
    if extractor_class is None:
        raise ValueError(f"No extractor available for source type: {source_type}")
    
    return extractor_class({})

__all__ = [
    'BaseExtractor',
    'ExtractorConfig',
    'ExtractorOutput',
    'PDFExtractor',
    'URLExtractor',
    # 'TextExtractor',
    # 'TextExtractorConfig',
    # 'ImageExtractor',
    # 'ImageExtractorConfig',
    # 'DocExtractor',
    # 'DocExtractorConfig',
    'get_extractor',
]