"""MarketPulse analytics: pure functions for comparison (TD07)."""


def index_by_date(prices):
    raise NotImplementedError


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
    raise NotImplementedError


def calculate_base_100(prices):
    raise NotImplementedError


def calculate_relative_performance(instrument_return, benchmark_return):
        return instrument_return - benchmark_return