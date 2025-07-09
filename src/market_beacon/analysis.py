from loguru import logger
from pydantic import BaseModel, Field

from .api.models import Candle, Trade


class TradeAnalysis(BaseModel):
    """Pydantic model for holding trade analysis results."""

    total_trades: int
    buy_trades: int
    sell_trades: int
    total_volume: float = Field(..., description="Total volume of all trades")
    buy_volume: float = Field(..., description="Volume of buy-side trades")
    sell_volume: float = Field(..., description="Volume of sell-side trades")
    vwap: float = Field(..., description="Volume-Weighted Average Price")


class CandleAnalysis(BaseModel):
    """Pydantic model for holding candlestick analysis results."""

    period_high: float = Field(..., description="Highest price in the candle period")
    period_low: float = Field(..., description="Lowest price in the candle period")
    price_change_percent: float = Field(
        ..., description="Percentage change from first open to last close"
    )
    simple_moving_average: float = Field(..., description="SMA of the closing prices")


class AnalysisResult(BaseModel):
    """A composite model for all analysis results."""

    symbol: str
    trade_stats: TradeAnalysis
    candle_stats: CandleAnalysis


def calculate_trade_stats(trades: list[Trade]) -> TradeAnalysis:
    """Calculates statistics from a list of recent trades."""
    if not trades:
        logger.warning("Trade list is empty, returning zeroed-out stats.")
        return TradeAnalysis(
            total_trades=0,
            buy_trades=0,
            sell_trades=0,
            total_volume=0.0,
            buy_volume=0.0,
            sell_volume=0.0,
            vwap=0.0,
        )

    buy_trades = [t for t in trades if t.side == "buy"]
    sell_trades = [t for t in trades if t.side == "sell"]

    total_volume = sum(t.size for t in trades)
    buy_volume = sum(t.size for t in buy_trades)
    sell_volume = sum(t.size for t in sell_trades)

    # Calculate Volume-Weighted Average Price (VWAP)
    weighted_price_sum = sum(t.price * t.size for t in trades)
    vwap = weighted_price_sum / total_volume if total_volume > 0 else 0.0

    return TradeAnalysis(
        total_trades=len(trades),
        buy_trades=len(buy_trades),
        sell_trades=len(sell_trades),
        total_volume=total_volume,
        buy_volume=buy_volume,
        sell_volume=sell_volume,
        vwap=vwap,
    )


def calculate_candle_stats(candles: list[Candle]) -> CandleAnalysis:
    """Calculates statistics from a list of candlestick data."""
    if not candles:
        logger.warning("Candle list is empty, returning zeroed-out stats.")
        return CandleAnalysis(
            period_high=0.0,
            period_low=0.0,
            price_change_percent=0.0,
            simple_moving_average=0.0,
        )

    # Ensure candles are sorted by time, just in case
    sorted_candles = sorted(candles, key=lambda c: c.timestamp)

    period_high = max(c.high for c in sorted_candles)
    period_low = min(c.low for c in sorted_candles)

    first_open = sorted_candles[0].open
    last_close = sorted_candles[-1].close
    price_change_percent = ((last_close - first_open) / first_open) * 100 if first_open > 0 else 0.0

    # Calculate Simple Moving Average (SMA) of the closing prices
    sma = sum(c.close for c in sorted_candles) / len(sorted_candles)

    return CandleAnalysis(
        period_high=period_high,
        period_low=period_low,
        price_change_percent=price_change_percent,
        simple_moving_average=sma,
    )


def run_analysis(symbol: str, trades: list[Trade], candles: list[Candle]) -> AnalysisResult:
    """
    Runs all analysis functions and returns a composite result.
    """
    logger.info(f"Running analysis for {symbol}...")
    trade_stats = calculate_trade_stats(trades)
    candle_stats = calculate_candle_stats(candles)

    return AnalysisResult(
        symbol=symbol,
        trade_stats=trade_stats,
        candle_stats=candle_stats,
    )
