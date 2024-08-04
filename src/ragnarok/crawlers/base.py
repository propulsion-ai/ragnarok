from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseCrawler(ABC):
    @abstractmethod
    def crawl(self, url: str, depth: int) -> List[Dict[str, Any]]:
        pass