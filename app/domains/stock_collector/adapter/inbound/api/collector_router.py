from typing import Optional, List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.domains.stock_collector.adapter.outbound.external.dart_collector_adapter import DartCollectorAdapter
from app.domains.stock_collector.adapter.outbound.external.news_collector_adapter import NewsCollectorAdapter
from app.domains.stock_collector.adapter.outbound.persistence.raw_article_repository_impl import RawArticleRepositoryImpl
from app.domains.stock_collector.application.request.collect_request import CollectRequest
from app.domains.stock_collector.application.response.article_response import ArticleResponse
from app.domains.stock_collector.application.response.collect_response import CollectResponse
from app.domains.stock_collector.application.usecase.collect_articles_usecase import CollectArticlesUseCase
from app.domains.stock_collector.application.usecase.get_articles_usecase import GetArticlesUseCase
from app.infrastructure.database.session import get_db

router = APIRouter(prefix="/stock-collector", tags=["stock-collector"])


@router.post("/collect", response_model=CollectResponse, status_code=200)
async def collect_articles(request: CollectRequest, db: Session = Depends(get_db)):
    repository = RawArticleRepositoryImpl(db)
    collectors = [DartCollectorAdapter(), NewsCollectorAdapter()]
    usecase = CollectArticlesUseCase(repository, collectors)
    return usecase.execute(request.symbol)


@router.get("/articles", response_model=List[ArticleResponse])
async def get_articles(
    symbol: Optional[str] = Query(default=None),
    source_type: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    repository = RawArticleRepositoryImpl(db)
    usecase = GetArticlesUseCase(repository)
    return usecase.execute(symbol=symbol, source_type=source_type)
