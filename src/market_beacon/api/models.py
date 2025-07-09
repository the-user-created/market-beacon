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
        # Using the modern `|` union type in isinstance
        if isinstance(v, int | float):
            return datetime.fromtimestamp(v / 1000.0)
        if isinstance(v, str) and v.isdigit():
            return datetime.fromtimestamp(int(v) / 1000.0)
        if isinstance(v, str):
            return isoparse(v)
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
        # Using the modern `|` union type in isinstance
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
        return cls(
            timestamp=datetime.fromtimestamp(int(data[0]) / 1000.0),
            open=float(data[1]),
            high=float(data[2]),
            low=float(data[3]),
            close=float(data[4]),
            volume=float(data[5]),
            quote_volume=float(data[6]),
        )
