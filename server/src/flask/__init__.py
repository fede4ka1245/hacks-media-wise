from io import BytesIO
from threading import Thread

from bson import ObjectId
from flask import Flask, request
from pandas import DataFrame, read_json

from src.processing.preprocessing import main as preprocess
from src.monogodb import mongodb_collection

from src.processing.process_data import process_data

flask_server = Flask(__name__)


@flask_server.route("/api/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "kirill yourself"
    file = request.files["file"]

    if file and file.filename != "":
        insertion = mongodb_collection.insert_one({"status": "uploading"})

        file_buffer = BytesIO()
        file.save(file_buffer)

        processing_thread = Thread(target=process_data(str(insertion.inserted_id), file_buffer), daemon=False)
        processing_thread.start()

        return str(insertion.inserted_id)
    else:
        return "smth didn't happen"


@flask_server.route("/api/upload/<report_id>/status", methods=["GET", "POST"])
def get_status(report_id: str):
    report = mongodb_collection.find_one({"_id": ObjectId(report_id)})
    if report is None:
        return "no report found", 404

    return report["status"]


@flask_server.route("/api/upload/<report_id>/result", methods=["GET", "POST"])
def get_results(report_id: str):
    report = mongodb_collection.find_one({"_id": ObjectId(report_id)})
    if report is None:
        return "no report found", 404

    df = read_json(report["data"])
    predicted_df = read_json(report["predicted_data"])
    chart_items = list()
    for feature_number, feature_name in enumerate(predicted_df.columns):
        if feature_number >= 1:
            chart_item = {"feature": feature_name, "chart_link": f"api/{report_id}/features_plots/{feature_number}"}
            chart_items.append(chart_item)

    feature_weights_chart_link = f"api/{report_id}/importances_plot"

    return {
        "feature_weights_chart_link": feature_weights_chart_link,
        "charts": chart_items
    }
