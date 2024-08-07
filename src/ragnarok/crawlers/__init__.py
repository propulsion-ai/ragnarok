from .base import BaseCrawler
from typing import Dict, Any

def get_crawler(type: str, config: Dict[str, Any]) -> BaseCrawler:
    if type == "playwright":
        from .playwright import PlaywrightCrawler
        return PlaywrightCrawler(config)
    else:
        raise ValueError(f"Unsupported crawler type: {type}")
    

__all__ = [
    'BaseCrawler',
    'get_crawler',
]