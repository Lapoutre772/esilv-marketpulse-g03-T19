"""Bloomberg-stage provider (TD10), APPROVED_SAMPLE mode.

The keys read here (observation_date, close_value, ...) are teaching wrapper
keys from the course fixture. They are not Bloomberg field mnemonics.
"""
import json
from pathlib import Path

ACCESS_MODE = "APPROVED_SAMPLE"
SAMPLE_PATH = Path("data/sample/bloomberg_reference_sample.json")

BLOOMBERG_IDENTIFIERS = {
    "AAPL": "AAPL US Equity",
    "SP500": "SPX Index",
}


def fetch_raw_bloomberg_history(identifier):
    """Raw input boundary: return the sample series for one identifier."""
    with open(SAMPLE_PATH, encoding="utf-8") as file:
        sample = json.load(file)

    for series in sample["series"]:
        if series["provider_identifier"] == identifier:
            return series

    raise ValueError(f"Identifier not found in approved sample: {identifier}")


def normalize_bloomberg_history(raw_data, canonical_ticker):
    """Normalization boundary: turn a raw series into canonical rows."""
    result = []
    for observation in raw_data["observations"]:
        result.append({
            "date": observation["observation_date"],
            "ticker": canonical_ticker,
            "open": float(observation["open_value"]),
            "high": float(observation["high_value"]),
            "low": float(observation["low_value"]),
            "close": float(observation["close_value"]),
            "volume": int(observation["volume_value"]),
        })

    return sorted(result, key=lambda r: r["date"])


def fetch_bloomberg_prices(canonical_ticker):
    if canonical_ticker not in BLOOMBERG_IDENTIFIERS:
        raise ValueError(f"Unknown canonical ticker: {canonical_ticker}")

    identifier = BLOOMBERG_IDENTIFIERS[canonical_ticker]
    raw_data = fetch_raw_bloomberg_history(identifier)
    rows = normalize_bloomberg_history(raw_data, canonical_ticker)

    if not rows:
        raise RuntimeError(f"No data in approved sample for {identifier}")

    return rows
