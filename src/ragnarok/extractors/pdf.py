# src/ragnarok/extractors/pdf.py
from .base import BaseExtractor, ExtractorConfig, ExtractorOutput
import pymupdf


class PDFExtractorConfig(ExtractorConfig):
    extract_metadata: bool = True


class PDFExtractor(BaseExtractor):
    def __init__(self, config: PDFExtractorConfig):
        super().__init__(config)

    def extract(self, source: str) -> ExtractorOutput:
        doc = pymupdf.open(source)
        text = ""
        for page in doc:
            text += page.get_text().encode("utf8")

        metadata = {}
        if self.config.extract_metadata:
            metadata = doc.metadata

        return ExtractorOutput(text=text, metadata=metadata)

    @classmethod
    def from_config(cls, config: PDFExtractorConfig) -> "PDFExtractor":
        return cls(config)
