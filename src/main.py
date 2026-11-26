from pathlib import Path
import csv
import json
import sys

# Allow "python src/main.py" as well as "python -m src.main".
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.analytics import (
    align_series,
    calculate_period_return,
    calculate_base_100,
    calculate_relative_performance
)
from src.providers.bloomberg_provider import ACCESS_MODE, fetch_bloomberg_prices
from src.providers.yahoo_provider import fetch_yahoo_prices

DATA_DIR = Path("data/sample")

# These starter values mirror config/settings.yml.
# settings.yml is a human-readable configuration contract in the CORE.
# Parsing YAML is optional and is not required by the 18-hour lab sequence.
LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def load_prices():
    with open(DATA_DIR / "prices.csv", encoding="utf-8") as file:
        return list(csv.DictReader(file))

def get_first_date(prices):
    return prices[0]["date"]

def get_last_date(prices):
    return prices[-1]["date"]


def filter_prices(prices, ticker):
    return [row for row in prices if row["ticker"] == ticker]

def get_first_close():
    with open(DATA_DIR / "prices.csv", encoding="utf-8") as file:
        prices= list(csv.DictReader(file))    
        print(float(prices[0]["close"]))







PROVIDER = "bloomberg"
LOOKBACK = "1mo"
INTERVAL = "1d"


def build_market_snapshot(provider=PROVIDER, lookback=LOOKBACK, interval=INTERVAL):
    """Shared application result used by the terminal (and by TD11)."""
    instruments = load_instruments()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]
    access_mode = None

    if provider == "bloomberg":
        # The approved sample is a fixed one-month daily fixture.
        instrument_prices = fetch_bloomberg_prices(instrument["ticker"])
        benchmark_prices = fetch_bloomberg_prices(benchmark["ticker"])
        access_mode = ACCESS_MODE
    elif provider == "yahoo":
        instrument_prices = fetch_yahoo_prices(instrument["ticker"], lookback, interval)
        benchmark_prices = fetch_yahoo_prices(benchmark["ticker"], lookback, interval)
    elif provider == "csv":
        prices = load_prices()
        instrument_prices = filter_prices(prices, instrument["ticker"])
        benchmark_prices = filter_prices(prices, benchmark["ticker"])
    else:
        raise ValueError(f"Unknown provider: {provider}")

    instrument_prices, benchmark_prices = align_series(
        instrument_prices,
        benchmark_prices
    )
    if not instrument_prices:
        raise RuntimeError("No common dates between instrument and benchmark")

    instrument_return = calculate_period_return(instrument_prices)
    benchmark_return = calculate_period_return(benchmark_prices)

    return {
        "provider": provider,
        "access_mode": access_mode,
        "lookback": lookback,
        "interval": interval,
        "instrument": instrument,
        "benchmark": benchmark,
        "instrument_prices": instrument_prices,
        "benchmark_prices": benchmark_prices,
        "instrument_return": instrument_return,
        "benchmark_return": benchmark_return,
        "relative_performance": calculate_relative_performance(
            instrument_return, benchmark_return
        ),
        "instrument_base_100": calculate_base_100(instrument_prices),
        "benchmark_base_100": calculate_base_100(benchmark_prices),
    }


def main():
    snapshot = build_market_snapshot()

    instrument = snapshot["instrument"]
    benchmark = snapshot["benchmark"]
    instrument_prices = snapshot["instrument_prices"]
    benchmark_prices = snapshot["benchmark_prices"]
    instrument_base = snapshot["instrument_base_100"]
    benchmark_base = snapshot["benchmark_base_100"]

    print("=== MarketPulse ===")
    print()
    print("Provider")
    if snapshot["access_mode"] == "APPROVED_SAMPLE":
        print("Bloomberg stage")
    else:
        print(snapshot["provider"].capitalize())
    if snapshot["access_mode"]:
        print()
        print("Access mode")
        print(snapshot["access_mode"])
    print()
    print("Instrument")
    print(f"{instrument['ticker']} - {instrument['name']}")
    print(f"Market: {instrument['market']}")
    print(f"Last price: {instrument_prices[-1]['close']} {instrument['currency']}")
    print()
    print("Benchmark")
    print(f"{benchmark['ticker']} - {benchmark['name']}")
    print(f"Market: {benchmark['market']}")
    print(f"Last level: {benchmark_prices[-1]['close']}")
    print()
    print(f"Period: {LOOKBACK_LABEL}")
    print(f"Interval: {INTERVAL_LABEL}")
    print()
    print("==Observations==")
    print(f"Instrument Observations : {instrument['ticker']}: {len(instrument_prices)}")
    print(f"Benchmark Observations : {benchmark['ticker']}: {len(benchmark_prices)}")
    print()
    print("==Observation dates==")
    print(f"{instrument['ticker']}: {get_first_date(instrument_prices)} -> {get_last_date(instrument_prices)}")
    print(f"{benchmark['ticker']}: {get_first_date(benchmark_prices)} -> {get_last_date(benchmark_prices)}")

    print()
    print("=== Comparison ===")
    print(f"Aligned sessions: {len(instrument_prices)}")
    print(f"{instrument['ticker']} return: {snapshot['instrument_return']:+.2f}%")
    print(f"{benchmark['ticker']} return: {snapshot['benchmark_return']:+.2f}%")
    print(f"Relative performance: {snapshot['relative_performance']:+.2f} percentage points")

    print()
    print("=== Base 100 ===")
    print(f"{instrument['ticker']}: {instrument_base[0]['value']:.2f} -> {instrument_base[-1]['value']:.2f}")
    print(f"{benchmark['ticker']}: {benchmark_base[0]['value']:.2f} -> {benchmark_base[-1]['value']:.2f}")


if __name__ == "__main__":
    main()
