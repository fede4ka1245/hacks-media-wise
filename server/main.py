from flask import Flask, request
from dash import Dash

from pymongo import MongoClient

from env import MONGODB_CONNECTION_URL
from processing.preprocessing import main as preprocess


mongodb_client = MongoClient(MONGODB_CONNECTION_URL)
mongodb_database = mongodb_client.get_database()
mongodb_collection = mongodb_database.get_collection("test_collection")

flask_server = Flask(__name__)


@flask_server.route("/new_record", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "kirill yourself"
    file = request.files["file"]

    if file and file.filename != "":
        data, ml_data, columns_with_not_enough_information, mean_std_info = preprocess(file)
        insertion = mongodb_collection.insert_one({
            "data": data,
            "ml_data": ml_data,
            "excluded_columns": columns_with_not_enough_information,
            "mean_std_info": mean_std_info
        })
        print(insertion)
        return insertion.inserted_id
    else:
        return "smth didn't happen"


dash_app = Dash(__name__, server=flask_server, use_pages=True)

if __name__ == '__main__':
    dash_app.run(debug=True)
