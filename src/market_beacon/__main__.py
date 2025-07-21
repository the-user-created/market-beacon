import argparse
import sys
from typing import get_args

from loguru import logger

from market_beacon.analysis import (
    calculate_order_book_stats,
    run_analysis,
)
from market_beacon.api import BitgetAPIError, BitgetClient
from market_beacon.api.client import MarketDataAPI
from market_beacon.config import settings


def main(args: list[str] | None = None) -> None:
    """
    Main entry point for the market-beacon application.

    This function parses command-line arguments, initializes the bot,
    and runs the main application logic.
    """
    # Get valid granularity choices directly from the type hint for robustness
    valid_granularity = get_args(MarketDataAPI.get_candles.__annotations__["granularity"])

    parser = argparse.ArgumentParser(description="Market Beacon Bot")
    parser.add_argument(
        "--symbol",
        type=str,
        default="BTCUSDT",
        help="The trading symbol to analyze (e.g., BTCUSDT).",
    )
    # --- Group for Technical Analysis ---
    ta_group = parser.add_argument_group("Technical Analysis Options")
    ta_group.add_argument(
        "--candle-limit",
        type=int,
        default=300,
        help="Number of candles for technical analysis (e.g., SMA, Ichimoku).",
    )
    ta_group.add_argument(
        "--granularity",
        type=str,
        default="1min",
        choices=valid_granularity,
        help="Candle granularity. From Bitget API.",
    )
    ta_group.add_argument(
        "--analysis-mode",
        type=str,
        default="fast",
        choices=["fast", "full"],
        help=(
            "'fast': (Default) Use candle data for efficient, approximated trade stats. "
            "'full': Fetch all individual trades for precise, but slower, stats."
        ),
    )

    # --- Group for Order Book Analysis ---
    ob_group = parser.add_argument_group("Order Book Options")
    ob_group.add_argument(
        "--get-orderbook",
        action="store_true",
        help="Fetch and analyze the order book instead of candles/trades.",
    )
    ob_group.add_argument(
        "--orderbook-level",
        type=str,
        default="step0",
        choices=["step0", "step1", "step2", "step3", "step4", "step5"],
        help="Order book aggregation level.",
    )
    ob_group.add_argument(
        "--orderbook-limit", type=int, default=50, help="Number of order book levels to fetch."
    )

    parsed_args = parser.parse_args(args)

    logger.info("Market Beacon bot starting...")
    logger.info(f"API Key loaded (first 5 chars): {settings.bitget_api_key[:5]}...")

    try:
        with BitgetClient(
            api_key=settings.bitget_api_key,
            secret_key=settings.bitget_api_secret,
            passphrase=settings.bitget_api_passphrase,
        ) as client:
            # --- Validate Symbol and Synchronize Time ---
            server_time = client.market.get_server_time()
            logger.info(f"Connected to Bitget. Server time: {server_time.server_time}")

            spot_symbols_list = client.market.get_supported_symbols()
            valid_symbols = set(spot_symbols_list)
            if parsed_args.symbol not in valid_symbols:
                logger.warning(
                    f"Symbol '{parsed_args.symbol}' not found in the list of supported symbols. "
                    "Proceeding anyway, but API calls may fail if the symbol is truly invalid."
                )
            else:
                logger.info(f"Symbol {parsed_args.symbol} validated against supported list.")

            # --- Main Logic: Execute one mode or the other ---
            if parsed_args.get_orderbook:
                logger.info(
                    f"Fetching order book for {parsed_args.symbol} "
                    f"(level: {parsed_args.orderbook_level}, limit: {parsed_args.orderbook_limit})"
                )
                order_book = client.market.get_order_book(
                    symbol=parsed_args.symbol,
                    level=parsed_args.orderbook_level,
                    limit=parsed_args.orderbook_limit,
                )
                order_book_stats = calculate_order_book_stats(order_book)
                logger.info("--- Order Book Analysis Complete ---")
                print(order_book_stats.model_dump_json(indent=2))

            else:  # Default to Technical Analysis
                logger.info(
                    f"Analyzing symbol: {parsed_args.symbol} "
                    f"in '{parsed_args.analysis_mode}' mode "
                    f"with granularity '{parsed_args.granularity}' "
                    f"({parsed_args.candle_limit} candles)"
                )

                # Always fetch candles as they are the basis for technical indicators
                candles = client.market.get_candles(
                    symbol=parsed_args.symbol,
                    granularity=parsed_args.granularity,
                    limit=parsed_args.candle_limit,
                )

                trades = []
                if candles:
                    # In 'full' mode, fetch all trades within the candle time range
                    if parsed_args.analysis_mode == "full":
                        start_time = candles[0].timestamp
                        end_time = candles[-1].timestamp
                        trades = client.market.get_trades(
                            symbol=parsed_args.symbol,
                            start_time=start_time,
                            end_time=end_time,
                        )
                else:
                    logger.warning("No candle data returned, skipping analysis.")

                # --- Run Analysis ---
                analysis_results = run_analysis(
                    symbol=parsed_args.symbol,
                    trades=trades,
                    candles=candles,
                    mode=parsed_args.analysis_mode,
                )

                # --- Display Results ---
                logger.info("--- Market Analysis Complete ---")
                results_json = analysis_results.model_dump_json(indent=2, exclude_none=True)
                print(results_json)

                # Save results to file
                with open("analysis_results.json", "w") as f:
                    f.write(results_json)

            logger.info("--- End of Analysis ---")

    except BitgetAPIError as e:
        logger.error(f"An API error occurred: {e}")
        logger.error(f"Response Body: {e.response_body}")
        sys.exit(1)
    except ValueError as e:
        logger.error(f"Configuration or data validation error: {e}")
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
