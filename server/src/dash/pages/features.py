import dash
from bson import ObjectId
from dash import html, dcc, callback, Input, Output
import plotly.express as px
from pandas import read_json

from re import compile as compile_regexp

from server.src.monogodb import mongodb_collection

PAGE_TEMPLATE_REGEXP = compile_regexp(r"/(\w+)/features_plots/(\d+)")


dash.register_page(__name__, path_template="/<report_id>/features_plots/<feature_number>")


def layout(report_id=None, feature_number=None, **kwargs):
    report = mongodb_collection.find_one({"_id": ObjectId(report_id)})
    if report is None:
        return html.Div(["Report not found"])
    else:
        return html.Div([
            dcc.Graph(id="graph-content"),
            dcc.Location(id="url", refresh=False),
        ])


@callback(
    Output("graph-content", "figure"),
    Input("url", "pathname")
)
def update_graph(pathname: str):
    report_id, feature_number_str = PAGE_TEMPLATE_REGEXP.match(pathname).groups()
    feature_number = int(feature_number_str)
    report = mongodb_collection.find_one({"_id": ObjectId(report_id)})
    df = read_json(report["data"])
    feature_name = df.columns[feature_number]
    return px.line(df[["Пеиод__Начало нед", feature_name]], x="Пеиод__Начало нед", y=feature_name)
