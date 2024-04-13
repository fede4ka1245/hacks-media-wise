from flask import Flask, request
from pandas import DataFrame

from server.processing.preprocessing import main as preprocess
from server.src.monogodb import mongodb_collection

flask_server = Flask(__name__)


@flask_server.route("/new_record", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "kirill yourself"
    file = request.files["file"]

    if file and file.filename != "":
        data, ml_data, columns_with_not_enough_information, mean_std_info = preprocess(file)
        insertion = mongodb_collection.insert_one({
            "data": data.to_json(),
            "ml_data": DataFrame(ml_data).to_json(),
            "excluded_columns": columns_with_not_enough_information,
            "mean_std_info": mean_std_info
        })
        return str(insertion.inserted_id)
    else:
        return "smth didn't happen"
