from datetime import datetime
from typing import Any

from dateutil.parser import isoparse
from pydantic import BaseModel, Field, field_validator


class APIResponse[T](BaseModel):
    """Generic Pydantic model for a standard Bitget API response structure."""

    code: str
    msg: str
    request_time: datetime = Field(alias="requestTime")
    data: T | None = None

    @field_validator("request_time", mode="before")
    @classmethod
    def convert_timestamp_to_datetime(cls, v: Any) -> datetime:
        if isinstance(v, int | float):
            # Assumes milliseconds
            return datetime.fromtimestamp(v / 1000.0)
        if isinstance(v, str) and v.isdigit():
            # Assumes milliseconds string
            return datetime.fromtimestamp(int(v) / 1000.0)
        if isinstance(v, str):
            # Fallback for ISO format strings
            return isoparse(v)
        return v


class ServerTime(BaseModel):
    """Represents the server time response."""

    server_time: datetime = Field(alias="serverTime")

    @field_validator("server_time", mode="before")
    @classmethod
    def convert_timestamp_to_datetime(cls, v: Any) -> datetime:
        if isinstance(v, str) and v.isdigit():
            return datetime.fromtimestamp(int(v) / 1000.0)
        return v


class SupportedSymbols(BaseModel):
    """Represents the response from the support-symbols endpoint."""

    spot_list: list[str] = Field(alias="spotList")
    future_list: list[str] = Field(alias="futureList")


class SymbolInfo(BaseModel):
    """Represents information about a single trading symbol."""

    symbol: str = Field(alias="symbolName")
    base_coin: str = Field(alias="baseCoin")
    quote_coin: str = Field(alias="quoteCoin")
    status: str
    price_precision: int = Field(alias="pricePrecision", default=8)
    quantity_precision: int = Field(alias="quantityPrecision", default=8)


class Ticker(BaseModel):
    """Represents ticker information for a symbol."""

    symbol: str
    last_price: float = Field(alias="lastPr")
    price_24h_high: float = Field(alias="high24h")
    price_24h_low: float = Field(alias="low24h")
    price_change_percent_24h: float = Field(alias="priceChangePercent")
    volume_24h: float = Field(alias="vol24h")
    volume_24h_usd: float = Field(alias="volUsd")
    timestamp: datetime = Field(alias="ts")

    @field_validator("timestamp", mode="before")
    @classmethod
    def convert_timestamp_to_datetime(cls, v: Any) -> datetime:
        if isinstance(v, str) and v.isdigit():
            return datetime.fromtimestamp(int(v) / 1000.0)
        return v


class Trade(BaseModel):
    """Represents a single trade execution."""

    trade_id: str = Field(alias="tradeId")
    price: float
    size: float
    side: str  # 'buy' or 'sell'
    timestamp: datetime = Field(alias="ts")

    @field_validator("timestamp", mode="before")
    @classmethod
    def convert_timestamp_to_datetime(cls, v: Any) -> datetime:
        if isinstance(v, int | float | str):
            return datetime.fromtimestamp(int(v) / 1000.0)
        return v


class Candle(BaseModel):
    """Represents a single candlestick (OHLCV)."""

    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    quote_volume: float

    @classmethod
    def from_list(cls, data: list[str]) -> "Candle":
        """Creates a Candle instance from a list of strings from the API."""
        if len(data) < 7:
            raise ValueError(f"Candle data list must have at least 7 elements, but got {len(data)}")
        return cls(
            timestamp=datetime.fromtimestamp(int(data[0]) / 1000.0),
            open=float(data[1]),
            high=float(data[2]),
            low=float(data[3]),
            close=float(data[4]),
            volume=float(data[5]),
            quote_volume=float(data[6]),
        )
