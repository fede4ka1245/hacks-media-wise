import dash
from bson import ObjectId
from dash import html, dcc
import plotly.express as px
from pandas import read_json

from re import compile as compile_regexp

from server.src.monogodb import mongodb_collection


dash.register_page(__name__, path_template="/<report_id>/importances_plot")


def layout(report_id=None, **kwargs):
    report = mongodb_collection.find_one({"_id": ObjectId(report_id)})

    if report is None:
        return html.Div(["Report not found"])
    else:
        df = read_json(report["data"])

        return dcc.Graph(figure=fig)
