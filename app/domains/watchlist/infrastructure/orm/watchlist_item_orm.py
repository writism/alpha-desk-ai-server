from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.infrastructure.database.session import Base


class WatchlistItemORM(Base):
    __tablename__ = "watchlist_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(6), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    market = Column(String(10), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
