import dash
import pandas as pd
from bson import ObjectId
from dash import html, dcc
import plotly.express as px
from pandas import read_json
import plotly.graph_objects as go

from src.monogodb import mongodb_collection
from src.processing.utils import confidence_interval

dash.register_page(__name__, path_template="/<report_id>/features_plots/<feature_number>")


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

        feature_name = predicted_df.columns[int(feature_number)]

        fig = px.scatter(df[[datetime_index, feature_name, "predicted"]], x=datetime_index, y=feature_name,
                         color="predicted", trendline="ols")
        fig.update_yaxes(visible=False, showticklabels=False)
        fig.update_xaxes(visible=False, showticklabels=False)
        fig.update_traces(mode="lines")
        fig.add_vline(x=predicted_df[datetime_index][0], annotation_text="Прогноз", line_dash="dot")
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

        # CI = confidence_interval(df[feature_name].dropna())
        #
        # fig.add_traces([
        #     go.Scatter(x=df[datetime_index], y=df[feature_name] + CI, mode="lines", showlegend=False,
        #                fillcolor="rgba(0,0,0,0)", line_color="rgba(0,0,0,0)"),
        #     go.Scatter(x=df[datetime_index], y=df[feature_name] - CI, mode='lines', line_color='rgba(0,0,0,0)',
        #                name='95% confidence interval', fill='tonexty', fillcolor='rgba(255, 0, 0, 0.2)')
        # ])

        return dcc.Graph(figure=fig)
