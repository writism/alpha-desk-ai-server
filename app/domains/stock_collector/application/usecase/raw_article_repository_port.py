from abc import ABC, abstractmethod
from typing import Optional, List

from app.domains.stock_collector.domain.entity.raw_article import RawArticle


class RawArticleRepositoryPort(ABC):
    @abstractmethod
    def save(self, article: RawArticle) -> RawArticle:
        pass

    @abstractmethod
    def find_by_dedup_key(self, source_type: str, source_doc_id: str) -> Optional[RawArticle]:
        pass

    @abstractmethod
    def find_all(self, symbol: Optional[str] = None, source_type: Optional[str] = None) -> List[RawArticle]:
        pass
