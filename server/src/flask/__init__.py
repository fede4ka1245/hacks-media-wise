from bson import ObjectId
from flask import Flask, request
from pandas import DataFrame, read_json

from server.processing.preprocessing import main as preprocess
from server.src.monogodb import mongodb_collection

flask_server = Flask(__name__)


@flask_server.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "kirill yourself"
    file = request.files["file"]

    if file and file.filename != "":
        data, ml_data, columns_with_not_enough_information, mean_std_info = preprocess(file)
        insertion = mongodb_collection.insert_one({
            "status": "processing",
            "data": data.to_json(),
            "ml_data": DataFrame(ml_data).to_json(),
            "excluded_columns": columns_with_not_enough_information,
            "mean_std_info": mean_std_info
        })
        return str(insertion.inserted_id)
    else:
        return "smth didn't happen"


@flask_server.route("/upload/<report_id>/status", methods=["GET", "POST"])
def get_status(report_id: str):
    report = mongodb_collection.find_one({"_id": ObjectId(report_id)})
    if report is None:
        return "no report found", 404

    return report["status"]


@flask_server.route("/upload/<report_id>/result", methods=["GET", "POST"])
def get_results(report_id: str):
    report = mongodb_collection.find_one({"_id": ObjectId(report_id)})
    if report is None:
        return "no report found", 404

    df = read_json(report["data"])
    chart_items = list()
    for feature_number, feature_name in enumerate(df.columns[3:], start=3):
        chart_item = {"feature": feature_name, "chart_link": f"/{report_id}/features_plots/{feature_number}"}
        chart_items.append(chart_item)

    feature_weights_chart_link = "/no_way"

    return {
        "feature_weights_chart_link": feature_weights_chart_link,
        "charts": chart_items
    }
