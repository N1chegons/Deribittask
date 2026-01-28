from typing import Optional

from fastapi import APIRouter
from fastapi.params import Query
from starlette import status
from starlette.exceptions import HTTPException

from src.currency.service import get_all_data_ticker, get_latest_price_ticker, get_filtered_prices_ticker
from src.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/ticker",
    tags=["Ticker"]
)

@router.get("/data/")
def get_all_data(ticker: str = Query(..., description="Введите тикер валют: BTCUSD/ETHUSD")):
    logger.info(f"Get data by: {ticker}")
    ticket_data = get_all_data_ticker(ticker)
    if not ticket_data:
        logger.warning(f"Data by {ticker} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"По тикеру {ticker} информации не найдено.")
    logger.info(f"Data by ticker {ticker} received successfully.")
    return ticket_data

@router.get("/latest_price/")
def get_latest_price(ticker: str = Query(..., description="Введите тикер валют: BTCUSD/ETHUSD")):
    logger.info(f"Get latest price by: {ticker}")
    latest_price_ticker = get_latest_price_ticker(ticker)
    if not latest_price_ticker:
        logger.warning(f"Data by {ticker} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"По тикеру {ticker} информации не найдено.")
    logger.info(f"Latest price by ticker {ticker} received successfully.")
    return latest_price_ticker

@router.get("/prices/filtered/")
def get_filtered_prices(ticker: str = Query(..., description="Введите тикер валют: BTCUSD/ETHUSD"), date_from: Optional[str] = Query(None, description="Начальная дата в формате YYYY-MM-DD"), date_to: Optional[str] = Query(None, description="Конечная дата в формате YYYY-MM-DD"), ):
    logger.info(f"Get filtered prices by: {ticker}")
    filtered_data = get_filtered_prices_ticker(ticker, date_from, date_to)
    if not filtered_data:
        logger.warning(f"Data by {ticker} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"По тикеру {ticker} информации не найдено.")
    logger.info(f"Filtered prices by ticker {ticker} received successfully. Arguments: {date_from} - {date_to}")
    return filtered_data


