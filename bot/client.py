import os
from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException

from bot.logging_config import setup_logging

load_dotenv()
logger = setup_logging("BinanceClient")


class BinanceFuturesClient:
    def __init__(self):
        self.client = Client(
            os.getenv("BINANCE_API_KEY"),
            os.getenv("BINANCE_API_SECRET"),
        )
        self.client.FUTURES_URL = "https://testnet.binancefuture.com"

    def create_order(self, **params):
        try:
            logger.info(f"API Request: {params}")

            response = self.client.futures_create_order(**params)

            logger.info(f"API Response: {response}")
            return response

        except (BinanceAPIException, BinanceOrderException) as e:
            logger.error(f"Binance error: {e}")
            raise

        except Exception as e:
            logger.exception("Unexpected error")
            raise
