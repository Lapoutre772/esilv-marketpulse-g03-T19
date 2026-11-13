from pathlib import Path
import csv
import json
from src.analytics import (
    align_series,
    calculate_period_return,
    calculate_base_100,
    calculate_relative_performance
)
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







PROVIDER = "yahoo"
def main():
    instruments = load_instruments()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    if PROVIDER == "yahoo":
        instrument_prices = fetch_yahoo_prices(instrument["ticker"])
        benchmark_prices = fetch_yahoo_prices(benchmark["ticker"])
    else:
        prices = load_prices()
        instrument_prices = filter_prices(prices, instrument["ticker"])
        benchmark_prices = filter_prices(prices, benchmark["ticker"])

    instrument_prices, benchmark_prices = align_series(
    instrument_prices,
    benchmark_prices
)   
    instrument_latest = instrument_prices[-1]
    benchmark_latest = benchmark_prices[-1]

    print("=== MarketPulse ===")
    print()
    print("Instrument")
    print(f"{instrument['ticker']} - {instrument['name']}")
    print(f"Market: {instrument['market']}")
    print(f"Last price: {instrument_latest['close']} {instrument['currency']}")
    print()
    print("Benchmark")
    print(f"{benchmark['ticker']} - {benchmark['name']}")
    print(f"Market: {benchmark['market']}")
    print(f"Last level: {benchmark_latest['close']}")
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

    instrument_return = calculate_period_return(instrument_prices)
    benchmark_return = calculate_period_return(benchmark_prices)

    relative = calculate_relative_performance(
        instrument_return, benchmark_return
    )

    instrument_base = calculate_base_100(instrument_prices)
    benchmark_base = calculate_base_100(benchmark_prices)

    print()
    print("=== Comparison ===")
    print(f"Aligned sessions: {len(instrument_prices)}")
    print(f"AAPL return: {instrument_return:+.2f}%")
    print(f"SP500 return: {benchmark_return:+.2f}%")
    print(f"Relative performance: {relative:+.2f} percentage points")

    print()
    print("=== Base 100 ===")
    print(f"AAPL: {instrument_base[0]['value']:.2f} -> {instrument_base[-1]['value']:.2f}")
    print(f"SP500: {benchmark_base[0]['value']:.2f} -> {benchmark_base[-1]['value']:.2f}")

def get_first_date(prices):
    return prices[0]["date"]


def get_last_date(prices):
    return prices[-1]["date"]
if __name__ == "__main__":
    main()
