from .base import BaseExtractor, ExtractorConfig, ExtractorOutput
from .pdf import PDFExtractor, PDFExtractorConfig
# from .text import TextExtractor, TextExtractorConfig
# from .image import ImageExtractor, ImageExtractorConfig
# from .doc import DocExtractor, DocExtractorConfig

# You can create a dictionary mapping file extensions to their respective extractors
EXTRACTOR_MAP = {
    '.pdf': PDFExtractor,
    # '.txt': TextExtractor,
    # '.jpg': ImageExtractor,
    # '.jpeg': ImageExtractor,
    # '.png': ImageExtractor,
    # '.doc': DocExtractor,
    # '.docx': DocExtractor,
}

def get_extractor(file_extension: str) -> BaseExtractor:
    """
    Factory function to get the appropriate extractor based on file extension.
    
    Args:
        file_extension (str): The file extension (including the dot)
    
    Returns:
        BaseExtractor: An instance of the appropriate extractor
    
    Raises:
        ValueError: If no extractor is available for the given file extension
    """
    extractor_class = EXTRACTOR_MAP.get(file_extension.lower())
    if extractor_class is None:
        raise ValueError(f"No extractor available for file extension: {file_extension}")
    
    # You might want to add configuration here if needed
    config = ExtractorConfig()  # or use a specific config if needed
    return extractor_class(config)

__all__ = [
    'BaseExtractor',
    'ExtractorConfig',
    'ExtractorOutput',
    'PDFExtractor',
    'PDFExtractorConfig',
    'TextExtractor',
    'TextExtractorConfig',
    'ImageExtractor',
    'ImageExtractorConfig',
    'DocExtractor',
    'DocExtractorConfig',
    'get_extractor',
]