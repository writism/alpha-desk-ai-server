from fastapi import HTTPException

from app.domains.watchlist.application.usecase.watchlist_repository_port import WatchlistRepositoryPort


class RemoveWatchlistUseCase:
    def __init__(self, repository: WatchlistRepositoryPort):
        self._repository = repository

    def execute(self, item_id: int) -> None:
        deleted = self._repository.delete_by_id(item_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="관심종목을 찾을 수 없습니다.")
