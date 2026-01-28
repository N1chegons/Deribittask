from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import insert, select

from src.currency.schemas import PriceResponse
from src.database import SyncSessionLocal
from src.currency.models import Ticker

# get
def get_all_data_ticker(ticker: str):
    with SyncSessionLocal() as session:
        query = select(Ticker).filter_by(ticker=ticker)
        result = session.execute(query)
        return [PriceResponse.model_validate(price) for price in result.scalars().all()]

def get_latest_price_ticker(ticker: str):
    with SyncSessionLocal() as session:
        query = select(Ticker.price).filter_by(ticker=ticker).order_by(Ticker.timestamp.desc())
        result = session.execute(query)
        latest = result.first()

        if latest:
            return {f"Последняя цена {ticker}": latest[0]}
        return None

def get_filtered_prices_ticker(
        ticker: str,
        date_from: str,
        date_to: str,
    ):
    with SyncSessionLocal() as session:
        query = select(Ticker.price).filter_by(ticker=ticker)

        try:
            if date_from:
                start_date = datetime.strptime(date_from, "%Y-%m-%d")
                query = query.filter(Ticker.created_at >= start_date)

            if date_to:
                end_date = datetime.strptime(date_to, "%Y-%m-%d")
                end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
                query = query.filter(Ticker.created_at <= end_date)
        except ValueError:
                raise HTTPException(status_code=400, detail="Неверный формат date_to. Используйте YYYY-MM-DD")

        result = session.execute(query.order_by(Ticker.created_at))
        prices = result.scalars().all()

        return {
            "Тикер: ": ticker,
            "Период с: ": date_from,
            "Период по: ": date_to,
            "Цена: ": prices
        }

# add
def add_price_in_db_ticker(ticker: str, price: float):
    with SyncSessionLocal() as session:
        stmt = insert(Ticker).values(
            ticker=ticker,
            price=price,
            timestamp=int(datetime.now().timestamp())
        )
        new_data = session.execute(stmt)

        try:

             session.commit()

        except Exception as e:

            return {"message": str(e)}