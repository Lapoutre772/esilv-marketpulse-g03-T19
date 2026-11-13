"""MarketPulse analytics: pure functions for comparison (TD07)."""

def index_by_date(prices):
    indexed = {}
    for row in prices:
        indexed[row["date"]] = row
    return indexed


def align_series(instrument_prices, benchmark_prices):
    instrument_dates = set()

    for row in instrument_prices:
        instrument_dates.add(row["date"])
    benchmark_dates = set()

    for row in benchmark_prices:
        benchmark_dates.add(row["date"])
    common_dates = instrument_dates & benchmark_dates
    common_dates = sorted(common_dates)
    aligned_instrument = []
    aligned_benchmark = []
    for date in common_dates:
        for row in instrument_prices:
            if row["date"] == date:
                aligned_instrument.append(row)
    for date in common_dates:
        for row in benchmark_prices:
            if row["date"] == date:
                aligned_benchmark.append(row)

    return aligned_instrument, aligned_benchmark





def calculate_period_return(prices):
    if not prices:
        raise ValueError("Cannot compute a return on an empty series")
    first_close = float(prices[0]["close"])
    last_close = float(prices[-1]["close"])
    if first_close == 0.0:
        raise ValueError("First close is zero: return is undefined")
    return ((last_close / first_close) - 1.0) * 100.0



def calculate_base_100(prices):
    if not prices:
        raise ValueError("La liste est vide")

    first_close = float(prices[0]["close"])

    if first_close == 0:
        raise ValueError("Le premier prix est égal à zéro")

    result = []

    for row in prices:
        current_close = float(row["close"])
        value = (current_close / first_close) * 100

        result.append({
            "date": row["date"],
            "ticker": row["ticker"],
            "value": value
        })

    return result



def calculate_relative_performance(instrument_return, benchmark_return):
    return instrument_return - benchmark_return
