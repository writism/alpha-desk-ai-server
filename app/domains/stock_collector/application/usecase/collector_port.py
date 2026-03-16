from abc import ABC, abstractmethod
from typing import List

from app.domains.stock_collector.domain.entity.raw_article import RawArticle


class CollectorPort(ABC):
    @abstractmethod
    def collect(self, symbol: str) -> List[RawArticle]:
        pass
