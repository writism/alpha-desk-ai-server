from typing import List

from app.domains.watchlist.application.response.watchlist_response import WatchlistItemResponse
from app.domains.watchlist.application.usecase.watchlist_repository_port import WatchlistRepositoryPort


class GetWatchlistUseCase:
    def __init__(self, repository: WatchlistRepositoryPort):
        self._repository = repository

    def execute(self) -> List[WatchlistItemResponse]:
        items = self._repository.find_all()

        return [
            WatchlistItemResponse(
                id=item.id,
                symbol=item.symbol,
                name=item.name,
                market=item.market,
                created_at=item.created_at,
            )
            for item in items
        ]
