import dash
import shap
from bson import ObjectId
from dash import html, dcc
from pandas import read_json
import matplotlib.pyplot as plt
from plotly.tools import mpl_to_plotly
from plotly.subplots import make_subplots

from src.monogodb import mongodb_collection


dash.register_page(__name__, path_template="/<report_id>/importances_plot")


def layout(report_id=None, **kwargs):
    report = mongodb_collection.find_one({"_id": ObjectId(report_id)})

    if report is None:
        return html.Div(["Report not found"])
    else:
        shap_values = read_json(report["shap_values"])
        val_values = read_json(report["val_values"])
        shap_values = shap_values.to_numpy()

        shap.summary_plot(shap_values, val_values, show=False)
        mpl_fig = plt.gcf()
        mpl_fig.set_figheight(5)
        mpl_fig.set_figwidth(10)

        tick_values, tick_texts = list(plt.yticks()[0]), list(map(lambda text: text._text, plt.yticks()[1]))

        plotly_fig = mpl_to_plotly(mpl_fig)
        plotly_fig.update_yaxes(tickvals=tick_values, ticktext=tick_texts, side="right")

        return dcc.Graph(figure=plotly_fig)
