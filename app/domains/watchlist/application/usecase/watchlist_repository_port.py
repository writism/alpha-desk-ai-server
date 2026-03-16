from abc import ABC, abstractmethod
from typing import Optional, List

from app.domains.watchlist.domain.entity.watchlist_item import WatchlistItem


class WatchlistRepositoryPort(ABC):
    @abstractmethod
    def save(self, item: WatchlistItem) -> WatchlistItem:
        pass

    @abstractmethod
    def find_by_symbol(self, symbol: str) -> Optional[WatchlistItem]:
        pass

    @abstractmethod
    def find_all(self) -> List[WatchlistItem]:
        pass

    @abstractmethod
    def delete_by_id(self, item_id: int) -> bool:
        pass
