import dash
import pandas as pd
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

        datetime_index = "Пеиод__Начало нед"
        df["predicted"] = 0
        predicted_df["predicted"] = 1
        df.set_index("Пеиод__Начало нед", inplace=True)
        predicted_df.set_index("Пеиод__Начало нед", inplace=True)

        df.update(predicted_df)
        df.reset_index(inplace=True)
        predicted_df.reset_index(inplace=True)

        feature_name = df.columns[int(feature_number)]

        fig = px.line(df[[datetime_index, feature_name, "predicted"]], x=datetime_index, y=feature_name,
                      color="predicted", line_shape="spline", markers=True)
        fig.add_vline(x=predicted_df[datetime_index][0], annotation_text="Пронгозируемая дата", line_dash="dot")
        fig.update_xaxes(type="date", range=[df[datetime_index].min(), predicted_df[datetime_index].max()])

        missing_data_intervals = []
        for i, value in enumerate(df[feature_name]):
            if pd.isna(value):
                if not missing_data_intervals:
                    missing_data_intervals.append([i, i])
                elif missing_data_intervals[-1][1] + 1 < i:
                    missing_data_intervals.append([i, i])
                else:
                    missing_data_intervals[-1][1] += 1

        for interval in missing_data_intervals:
            fig.add_vrect(x0=df[datetime_index][interval[0]], x1=df[datetime_index][interval[1]], row="all", col=1,
                          fillcolor="red", opacity=0.25, line_width=0)

        return dcc.Graph(figure=fig)
