# src/ragnarok/extractors/pdf.py
import os
from .base import BaseExtractor, ExtractorOutput
import pymupdf as fitz

class PDFExtractor(BaseExtractor):
    def __init__(self, config: dict):
        super().__init__(config)
        self.extract_metadata = config.get("extract_metadata", True)

    def extract(self, source: str, *args, **kwargs) -> ExtractorOutput:
        text, metadata = self.extract_pdf(source)
        metadata["filename"] = os.path.basename(source)
        return [ExtractorOutput(text=text, metadata=metadata)]

    @classmethod
    def from_config(cls, config: dict) -> "PDFExtractor":
        return cls(config)

    def extract_pdf(self, file):
        metadata = {}
        text = ""
        with fitz.open(file, filetype="pdf") as doc:
            metadata = doc.metadata
            for page in doc:
                text += page.get_text()
        return text, metadata
