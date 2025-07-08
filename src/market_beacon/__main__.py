import argparse
import sys

from loguru import logger

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

    # TODO: Initialize API client
    # TODO: Fetch trade data
    # TODO: Calculate statistics
    # TODO: Print or store results

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
