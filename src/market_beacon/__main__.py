import argparse
import sys

from loguru import logger

from market_beacon.analysis import run_analysis
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
    # Add more arguments for analysis parameters
    parser.add_argument(
        "--trade-limit", type=int, default=100, help="Number of recent trades to analyze."
    )
    parser.add_argument("--candle-limit", type=int, default=20, help="Number of candles for SMA.")
    parser.add_argument(
        "--granularity", type=str, default="1h", help="Candle granularity (e.g., 5m, 1h, 1D)."
    )
    parsed_args = parser.parse_args(args)

    logger.info("Market Beacon bot starting...")
    logger.info(f"API Key loaded (first 5 chars): {settings.bitget_api_key[:5]}...")
    logger.info(
        f"Analyzing symbol: {parsed_args.symbol} "
        f"({parsed_args.trade_limit} trades, {parsed_args.candle_limit} candles)"
    )

    try:
        with BitgetClient(
            api_key=settings.bitget_api_key,
            secret_key=settings.bitget_api_secret,
            passphrase=settings.bitget_api_passphrase,
        ) as client:
            # --- Fetch Data ---
            trades = client.get_spot_trades(
                symbol=parsed_args.symbol, limit=parsed_args.trade_limit
            )
            candles = client.get_spot_candles(
                symbol=parsed_args.symbol,
                granularity=parsed_args.granularity,
                limit=parsed_args.candle_limit,
            )

            # --- Run Analysis ---
            analysis_results = run_analysis(
                symbol=parsed_args.symbol, trades=trades, candles=candles
            )

            # --- Display Results ---
            logger.info("--- Market Analysis Complete ---")
            # Use model_dump_json for clean, structured output
            results_json = analysis_results.model_dump_json(indent=2)
            # Log the JSON directly. Loguru will handle the formatting.
            print(results_json)
            logger.info("--- End of Analysis ---")

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
