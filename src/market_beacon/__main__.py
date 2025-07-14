import argparse
import sys

from loguru import logger

from market_beacon.analysis import calculate_order_book_stats, run_analysis
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
    parser.add_argument(
        "--trade-limit", type=int, default=100, help="Number of recent trades to analyze."
    )
    parser.add_argument(
        "--candle-limit",
        type=int,
        default=300,
        help="Number of candles for technical analysis (e.g., SMA, Ichimoku).",
    )
    parser.add_argument(
        "--granularity",
        type=str,
        default="1h",
        help="Candle granularity (e.g., 5m, 1H, 1D).",
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
            # TODO: Needs to allow brand-new symbols that are not yet in the list
            if parsed_args.symbol not in valid_symbols:
                logger.error(
                    f"Invalid symbol '{parsed_args.symbol}'. Please choose a valid symbol."
                )
                sys.exit(1)
            logger.info(f"Symbol {parsed_args.symbol} validated successfully.")

            logger.info(f"Fetching order book for {parsed_args.symbol}...")
            order_book = client.market.get_order_book(
                symbol=parsed_args.symbol,
                level=parsed_args.orderbook_level,
                limit=parsed_args.orderbook_limit,
            )
            order_book_stats = calculate_order_book_stats(order_book)

            logger.info("--- Order Book Analysis Complete ---")
            results_json = order_book_stats.model_dump_json(indent=2)
            print(results_json)
            logger.info("--- End of Analysis ---")

            # --- Fetch Data using new namespaced client ---
            logger.info(
                f"Analyzing symbol: {parsed_args.symbol} "
                f"({parsed_args.trade_limit} trades, {parsed_args.candle_limit} candles)"
            )

            trades = client.market.get_trades(
                symbol=parsed_args.symbol, limit=parsed_args.trade_limit
            )
            candles = client.market.get_candles(
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
            results_json = analysis_results.model_dump_json(indent=2)
            print(results_json)  # Print JSON to stdout for potential piping
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
