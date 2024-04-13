import dash
from bson import ObjectId
from dash import html, dcc, callback, Input, Output
import plotly.express as px
from pandas import read_json

from re import compile as compile_regexp

from server.src.monogodb import mongodb_collection

PAGE_TEMPLATE_REGEXP = compile_regexp(r"/(\w+)/features")


dash.register_page(__name__, path_template="/<report_id>/features")


def layout(report_id=None, **kwargs):
    report = mongodb_collection.find_one({"_id": ObjectId(report_id)})
    if report is None:
        return html.Div(["Report not found"])
    else:
        df = read_json(report["data"])
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
    report_id = PAGE_TEMPLATE_REGEXP.match(pathname).groups()[0]
    report = mongodb_collection.find_one({"_id": ObjectId(report_id)})
    df = read_json(report["data"])
    return px.line(df[["Пеиод__Начало нед", value]], x="Пеиод__Начало нед", y=value)
