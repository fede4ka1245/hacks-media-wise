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
        predicted_df = read_json(report["predicted_data"])

        df["predicted"] = 0
        predicted_df["predicted"] = 1
        df.set_index("Пеиод__Начало нед", inplace=True)
        predicted_df.set_index("Пеиод__Начало нед", inplace=True)

        df.update(predicted_df)
        df.reset_index(inplace=True)
        predicted_df.reset_index(inplace=True)

        feature_name = df.columns[int(feature_number)]

        fig = px.line(df[["Пеиод__Начало нед", feature_name, "predicted"]], x="Пеиод__Начало нед", y=feature_name, color="predicted", line_shape="spline", markers=True)
        fig.add_vline(x=predicted_df["Пеиод__Начало нед"][0], annotation_text="Пронгозируемая дата", line_dash="dot")

        return dcc.Graph(figure=fig)
