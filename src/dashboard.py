from dash import Dash, dcc, html
import plotly.graph_objects as go

from main import build_market_snapshot


def build_information(snapshot):
    """Student 2: context and the three performance values."""
    return html.Div("Context and performance: to do")


def build_figure(snapshot):
    """Student 3: base-100 chart."""
    return go.Figure()


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
