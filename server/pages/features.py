import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd

from re import compile as compile_regexp

PAGE_TEMPLATE_REGEXP = compile_regexp(r"/(\d+)/features")


dash.register_page(__name__, path_template="/<report_id>/features")


df = pd.read_csv("/home/lukra/downloads/Telegram Desktop/viz_data.csv")


def layout(report_id=None, **kwargs):
    features = df.columns.values[3:]
    return html.Div([
        f"ID: {report_id}.",
        dcc.Dropdown(features, features[0], id="dropdown-selection"),
        dcc.Graph(id="graph-content"),
        dcc.Location(id="url", refresh=False),
    ])


@callback(
    Output("graph-content", "figure"),
    Input("dropdown-selection", "value"),
    Input("url", "pathname")
)
def update_graph(value, pathname: str):
    report_id = int(PAGE_TEMPLATE_REGEXP.match(pathname).groups()[0])
    print(report_id)
    return px.line(df[["Пеиод__Начало нед", value]], x="Пеиод__Начало нед", y=value)
