import aiohttp
import requests
from datetime import datetime
import nest_asyncio
from src.currency.celery_config import celery_app
from src.currency.service import add_price_in_db_ticker
from src.logger import get_logger

AsyncClient = aiohttp.ClientSession
nest_asyncio.apply()

logger = get_logger(__name__)

@celery_app.task(name='fetch_prices_task')
def fetch_and_save_prices():
    logger.info("Celery has started.")
    try:
        # 1. BTC request
        logger.info("Request to BTC")
        btc_response = requests.get(
            "https://test.deribit.com/api/v2/public/get_index_price",
            params={"index_name": "btc_usd"},
            timeout=10
        )
        if btc_response.status_code == 200:
            btc_data = btc_response.json()
            btc_price = btc_data["result"]["index_price"]
            logger.info(f"ETH price: ${btc_price}")
        else:
            logger.error(f"❌ BTC error: {btc_response.text}")
            btc_price = None

        # 2. ETH request
        logger.info("Request to ETH")
        eth_response = requests.get(
            "https://test.deribit.com/api/v2/public/get_index_price",
            params={"index_name": "eth_usd"},
            timeout=10
        )
        if eth_response.status_code == 200:
            eth_data = eth_response.json()
            eth_price = eth_data["result"]["index_price"]
            logger.info(f"ETH price: ${eth_price}")
        else:
            logger.error(f"❌ ETH error: {eth_response.text}")
            eth_price = None

        # Add to db
        if btc_price is not None:
            try:
                add_price_in_db_ticker("BTCUSD", btc_price)
                logger.info("Save to db: BTC")
            except Exception as e:
                logger.error(f"❌ Error save to db BTC: {e}")

        if eth_price is not None:
            try:
                add_price_in_db_ticker("ETHUSD", eth_price)
                logger.info("Save to db: ETH")
            except Exception as e:
                logger.error(f"❌ Error save to db ETH: {e}")

        logger.info("Celery task was completed successfully")

        return {
            "success": True,
            "btc": btc_price,
            "eth": eth_price,
            "timestamp": datetime.now().isoformat()
        }

    except requests.exceptions.Timeout:
        logger.error(f"❌ Timeout Error")
        return {"error": "Request timeout"}
    except requests.exceptions.ConnectionError:
        logger.error(f"❌ Connection error")
        return {"error": "Connection error"}
    except Exception as e:
        print(f"❌ ОШИБКА: {type(e).__name__}: {e}")
        logger.error(f"❌ ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}