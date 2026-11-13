
import yfinance as yf

CANONICAL_TO_YAHOO = {
    "AAPL": "AAPL",
    "SP500": "^GSPC"
}

def fetch_yahoo_prices(canonical_ticker, lookback="1mo", interval="1d"):
    symbol = CANONICAL_TO_YAHOO[canonical_ticker]

    data = yf.download(
        symbol,
        period=lookback,
        interval=interval,
        auto_adjust=True,
        multi_level_index=False,
        progress=False
    )

    result = []

    for date, row in data.iterrows():
        result.append({
            "date": date.strftime("%Y-%m-%d"),
            "ticker": canonical_ticker,
            "open": float(row["Open"]),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"]),
            "volume": int(row["Volume"])
        })

    return result
