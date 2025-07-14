import json
from collections.abc import Callable
from types import TracebackType
from typing import Any, Literal

import requests
from loguru import logger

from .auth import generate_signature, get_timestamp_ms
from .exceptions import BitgetAPIError, BitgetAPIRequestError
from .models import APIResponse, Candle, OrderBook, ServerTime, SupportedSymbols, Ticker, Trade


class MarketDataAPI:
    """Namespace for public market data endpoints."""

    def __init__(self, request_func: Callable[..., Any]):
        self._request = request_func

    def get_server_time(self) -> ServerTime:
        """
        Gets the current exchange server time.
        Endpoint: GET /public/time
        """
        logger.info("Fetching server time...")
        data = self._request("GET", "/public/time")
        return ServerTime.model_validate(data)

    def get_supported_symbols(self) -> list[str]:
        """
        Gets a list of all available spot trading pair names.
        Endpoint: GET /spot/market/support-symbols
        """
        logger.info("Fetching all supported spot symbols...")
        data = self._request("GET", "/spot/market/support-symbols")
        supported_symbols = SupportedSymbols.model_validate(data)
        return supported_symbols.spot_list

    def get_ticker(self, symbol: str) -> Ticker:
        """
        Gets ticker information for a specific symbol.
        Endpoint: GET /spot/market/ticker
        """
        logger.info(f"Fetching ticker for {symbol}...")
        params = {"symbol": symbol}
        data = self._request("GET", "/spot/market/ticker", params=params)
        # Ticker data for a single symbol is returned as a list with one item
        if not data:
            raise BitgetAPIError(f"No ticker data returned for symbol {symbol}")
        return Ticker.model_validate(data[0])

    def get_trades(self, symbol: str, limit: int = 100) -> list[Trade]:
        """
        Retrieves the most recent public trades for a given spot symbol.
        Endpoint: GET /spot/market/fills
        """
        logger.info(f"Fetching last {limit} trades for {symbol}...")
        params = {"symbol": symbol, "limit": limit}
        data = self._request("GET", "/spot/market/fills", params=params)
        return [Trade.model_validate(trade) for trade in data]

    def get_candles(
        self,
        symbol: str,
        granularity: Literal[
            "1min",
            "3min",
            "5min",
            "15min",
            "30min",
            "1h",
            "4h",
            "6h",
            "12h",
            "1day",
            "1week",
            "1M",
            "6Hutc",
            "12Hutc",
            "1Dutc",
            "3Dutc",
            "1Wutc",
            "1Mutc",
        ],
        limit: int = 100,
    ) -> list[Candle]:
        """
        Retrieves historical candlestick data for a given spot symbol.
        Endpoint: GET /spot/market/candles
        """
        logger.info(f"Fetching last {limit} candles ({granularity}) for {symbol}...")
        params = {"symbol": symbol, "granularity": granularity, "limit": limit}
        data = self._request("GET", "/spot/market/candles", params=params)
        # Data is already in chronological order (oldest to newest)
        return [Candle.from_list(candle_data) for candle_data in data]

    def get_order_book(
        self,
        symbol: str,
        level: Literal["step0", "step1", "step2", "step3", "step4", "step5"] = "step0",
        limit: int = 50,
    ) -> OrderBook:
        """
        Retrieves the order book for a given spot symbol.
        Endpoint: GET /spot/market/orderbook

        Args:
            symbol: The trading pair symbol (e.g., BTCUSDT).
            level: The price aggregation level. 'step0' is the most granular.
            limit: The number of price levels to return (max 400 for step0).
        """
        logger.info(f"Fetching order book for {symbol} (level: {level}, limit: {limit})...")
        params = {"symbol": symbol, "type": level, "limit": limit}
        data = self._request("GET", "/spot/market/orderbook", params=params)
        return OrderBook.model_validate(data)


class BitgetClient:
    """
    A high-performance, typed client for the Bitget V2 API.
    """

    BASE_URL = "https://api.bitget.com"

    def __init__(self, api_key: str, secret_key: str, passphrase: str):
        if not all([api_key, secret_key, passphrase]):
            raise ValueError("API key, secret key, and passphrase must be provided.")

        self._api_key = api_key
        self._secret_key = secret_key
        self._passphrase = passphrase
        self._session = requests.Session()

        # --- API Namespaces ---
        self.market = MarketDataAPI(self._request)

    def __enter__(self) -> "BitgetClient":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()

    def close(self) -> None:
        """Closes the underlying requests session."""
        self._session.close()
        logger.debug("Bitget API client session closed.")

    def _create_headers(
        self, method: str, request_path: str, body: str | bytes, timestamp: str
    ) -> dict[str, str]:
        """Creates the necessary headers for an API request."""
        body_str = body.decode() if isinstance(body, bytes) else body
        signature = generate_signature(timestamp, method, request_path, body_str, self._secret_key)
        return {
            "ACCESS-KEY": self._api_key,
            "ACCESS-SIGN": signature,
            "ACCESS-TIMESTAMP": timestamp,
            "ACCESS-PASSPHRASE": self._passphrase,
            "Content-Type": "application/json",
            "locale": "en-US",
        }

    def _request(self, method: str, endpoint: str, params: dict[str, Any] | None = None) -> Any:
        """Generic method to make a request to the Bitget API."""
        request_path = f"/api/v2{endpoint}"
        url = self.BASE_URL + request_path

        is_post = method.upper() == "POST"
        body = json.dumps(params) if is_post and params else ""
        query_params = params if not is_post else None
        timestamp = get_timestamp_ms()

        # All requests, including public ones, are signed for simplicity and consistency.
        # Bitget's public endpoints ignore auth headers if not needed.
        headers = self._create_headers(method, request_path, body, timestamp)

        try:
            response = self._session.request(
                method=method, url=url, params=query_params, data=body, headers=headers, timeout=10
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise BitgetAPIRequestError(response=e.response) from e
        except requests.exceptions.RequestException as e:
            raise BitgetAPIError(f"HTTP Request failed: {e}") from e

        parsed_response = APIResponse[Any].model_validate(response.json())

        if parsed_response.code != "00000":
            # Pass the original response to the exception for full context
            raise BitgetAPIRequestError(response)

        return parsed_response.data
