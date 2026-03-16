from typing import List

from app.domains.stock_collector.application.usecase.collector_port import CollectorPort
from app.domains.stock_collector.application.usecase.raw_article_repository_port import RawArticleRepositoryPort
from app.domains.stock_collector.application.response.collect_response import CollectResponse, CollectedItem
from app.domains.stock_collector.domain.entity.raw_article import RawArticle


class CollectArticlesUseCase:
    def __init__(
        self,
        repository: RawArticleRepositoryPort,
        collectors: List[CollectorPort],
    ):
        self._repository = repository
        self._collectors = collectors

    def execute(self, symbol: str) -> CollectResponse:
        collected_items = []
        total_collected = 0
        total_skipped = 0

        for collector in self._collectors:
            articles = collector.collect(symbol)

            for article in articles:
                existing = self._repository.find_by_dedup_key(
                    article.source_type, article.source_doc_id
                )
                if existing:
                    total_skipped += 1
                    continue

                saved = self._repository.save(article)
                collected_items.append(
                    CollectedItem(
                        id=saved.id,
                        source_type=saved.source_type,
                        title=saved.title,
                    )
                )
                total_collected += 1

        return CollectResponse(
            symbol=symbol,
            total_collected=total_collected,
            total_skipped=total_skipped,
            items=collected_items,
        )
