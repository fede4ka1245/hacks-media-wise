import dash
import shap
from bson import ObjectId
from dash import html, dcc
from pandas import read_json
import matplotlib.pyplot as plt
from plotly.tools import mpl_to_plotly
import numpy as np
from shap import Explanation

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
        fig = plt.gcf()
        fig.set_figheight(5)
        fig.set_figwidth(10)
        fig = mpl_to_plotly(fig)
        # shap.plots.beeswarm(Explanation(shap_values), color="red")

        return dcc.Graph(figure=fig)
