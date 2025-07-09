import argparse
import sys

from loguru import logger

from market_beacon.api import BitgetAPIError, BitgetClient
from market_beacon.config import settings


def main(args: list[str] | None = None) -> None:
    """
    Main entry point for the market-beacon application.

    This function parses command-line arguments, initializes the bot,
    and runs the main application logic.
    """
    parser = argparse.ArgumentParser(description="Market Beacon Bot")
    parser.add_argument(
        "--symbol",
        type=str,
        default="BTCUSDT",
        help="The trading symbol to analyze (e.g., BTCUSDT).",
    )
    parsed_args = parser.parse_args(args)

    logger.info("Market Beacon bot starting...")
    logger.info(f"API Key loaded (first 5 chars): {settings.bitget_api_key[:5]}...")
    logger.info(f"Analyzing symbol: {parsed_args.symbol}")

    try:
        with BitgetClient(
            api_key=settings.bitget_api_key,
            secret_key=settings.bitget_api_secret,
            passphrase=settings.bitget_api_passphrase,
        ) as client:
            # --- Fetch trade data ---
            trades = client.get_spot_trades(symbol=parsed_args.symbol, limit=5)
            logger.info(f"Successfully fetched {len(trades)} recent trades.")
            for trade in trades:
                logger.info(
                    f"  - Trade ID: {trade.trade_id}, Side: {trade.side}, "
                    f"Price: {trade.price}, Size: {trade.size}, Time: {trade.timestamp}"
                )

            # --- Fetch candle data ---
            candles = client.get_spot_candles(symbol=parsed_args.symbol, granularity="1h", limit=3)
            logger.info(f"Successfully fetched {len(candles)} recent 1H candles.")
            for candle in candles:
                logger.info(
                    f"  - Time: {candle.timestamp}, Open: {candle.open}, High: {candle.high}, "
                    f"Low: {candle.low}, Close: {candle.close}, Volume: {candle.volume}"
                )

            # TODO: Calculate statistics from the 'trades' and 'candles' lists
            # TODO: Print or store results

    except BitgetAPIError as e:
        logger.error(f"An API error occurred: {e}")
        logger.error(f"Response Body: {e.response_body}")
        sys.exit(1)
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)

    logger.info("Market Beacon bot finished.")


def run():
    """
    Wrapper for main() to be used as the entry point for the module.
    This helps in managing system exit codes and arguments gracefully.
    """
    try:
        main()
    except Exception as e:
        logger.exception("An unhandled exception occurred: {}", e)
        sys.exit(1)


if __name__ == "__main__":
    run()
