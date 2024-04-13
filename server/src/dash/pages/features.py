import dash
from bson import ObjectId
from dash import html, dcc
import plotly.express as px
from pandas import read_json

from src.monogodb import mongodb_collection


dash.register_page(__name__, path_template="/api/<report_id>/features_plots/<feature_number>")


def layout(report_id=None, feature_number=None, **kwargs):
    report = mongodb_collection.find_one({"_id": ObjectId(report_id)})

    if report is None:
        return html.Div(["Report not found"])
    else:
        df = read_json(report["data"])
        feature_name = df.columns[int(feature_number)]
        fig = px.line(df[["Пеиод__Начало нед", feature_name]], x="Пеиод__Начало нед", y=feature_name)

        return dcc.Graph(figure=fig)
