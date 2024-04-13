from bson import ObjectId
from src.monogodb import mongodb_collection
from pandas import read_json, DataFrame

from .predict_catboost import make_predict
from .preprocessing import main as preprocess


def process_data(report_id: str, file):
    def function():
        data, ml_data, columns_with_not_enough_information, mean_std_info = preprocess(file)

        mongodb_collection.update_one({"_id": ObjectId(report_id)}, {"$set": {
            "status": "processing",
            "data": data.to_json(),
            "ml_data": DataFrame(ml_data).to_json(),
            "excluded_columns": columns_with_not_enough_information,
            "mean_std_info": mean_std_info
        }})

        predicted_data, shap_values = make_predict(ml_data, mean_std_info)

        mongodb_collection.update_one({"_id": ObjectId(report_id)}, {"$set": {
            "status": "ready",
            "data": data.to_json(),
            "shap_values": DataFrame(shap_values).to_json(),
            "predicted_data": predicted_data.to_json(),
            "ml_data": DataFrame(ml_data).to_json(),
            "excluded_columns": columns_with_not_enough_information,
            "mean_std_info": mean_std_info
        }})

    return function
