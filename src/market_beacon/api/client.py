import json
from typing import Any

import requests
from loguru import logger

from .auth import generate_signature, get_timestamp_ms
from .exceptions import BitgetAPIError, BitgetAPIRequestError
from .models import APIResponse, Candle, Trade


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

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Closes the underlying requests session."""
        self._session.close()
        logger.debug("Bitget API client session closed.")

    def _create_headers(self, method: str, request_path: str, body: str | bytes) -> dict[str, str]:
        """Creates the necessary headers for a private API request."""
        timestamp = get_timestamp_ms()
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
        """
        Generic method to make a request to the Bitget API.
        """
        request_path = f"/api/v2{endpoint}"
        url = self.BASE_URL + request_path

        body = json.dumps(params) if method.upper() == "POST" and params else ""
        headers = self._create_headers(method, request_path, body)
        query_params = params if method.upper() == "GET" else None

        try:
            response = self._session.request(
                method=method,
                url=url,
                params=query_params,
                data=body,
                headers=headers,
                timeout=10,
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise BitgetAPIRequestError(response=e.response) from e
        except requests.exceptions.RequestException as e:
            raise BitgetAPIError(f"HTTP Request failed: {e}") from e

        parsed_response = APIResponse[Any].model_validate(response.json())

        if parsed_response.code != "00000":
            raise BitgetAPIRequestError(response)

        return parsed_response.data

    # --------------------------------------------------------------------------
    # Public Market Data Endpoints
    # --------------------------------------------------------------------------
    def get_spot_trades(self, symbol: str, limit: int = 100) -> list[Trade]:
        """
        Retrieves the most recent public trades for a given spot symbol.
        Endpoint: GET /spot/market/fills
        """
        logger.info(f"Fetching last {limit} trades for {symbol}...")
        params = {"symbol": symbol, "limit": limit}
        data = self._request("GET", "/spot/market/fills", params=params)
        return [Trade.model_validate(trade) for trade in data]

    def get_spot_candles(self, symbol: str, granularity: str, limit: int = 100) -> list[Candle]:
        """
        Retrieves historical candlestick data for a given spot symbol.
        Endpoint: GET /spot/market/candles
        Args:
            granularity: Bar size. Valid values: [1m, 5m, 15m, 30m, 1h, 4h, 12h, 1D, 1W]
        """
        logger.info(f"Fetching last {limit} candles ({granularity}) for {symbol}...")
        params = {"symbol": symbol, "granularity": granularity, "limit": limit}
        data = self._request("GET", "/spot/market/candles", params=params)
        return [Candle.from_list(candle_data) for candle_data in data]
