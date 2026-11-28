from dash import Dash, dcc, html
import plotly.graph_objects as go

from main import build_market_snapshot


def build_information(snapshot):
    """Student 2: context and the three performance values."""
    return html.Div("Context and performance: to do")


def build_figure(snapshot):
    """Student 3: base-100 chart."""
    instrument = snapshot["instrument"]
    benchmark = snapshot["benchmark"]
    instrument_base_100 = snapshot["instrument_base_100"]
    benchmark_base_100 = snapshot["benchmark_base_100"]

    figure = go.Figure()

    figure.add_trace(
        go.Scatter(
            x=[row["date"] for row in instrument_base_100],
            y=[row["value"] for row in instrument_base_100],
            mode="lines",
            name=instrument["ticker"],
        )
    )

    figure.add_trace(
        go.Scatter(
            x=[row["date"] for row in benchmark_base_100],
            y=[row["value"] for row in benchmark_base_100],
            mode="lines",
            name=benchmark["ticker"],
        )
    )

    figure.update_layout(
        title="Instrument vs Benchmark - Base 100",
        xaxis_title="Date",
        yaxis_title="Base 100",
    )

    return figure


snapshot = build_market_snapshot()
app = Dash(__name__)
app.layout = html.Div(
    [
        html.H1("MarketPulse"),
        build_information(snapshot),
        dcc.Graph(figure=build_figure(snapshot)),
    ]
)


if __name__ == "__main__":
    app.run(debug=False)
