from bson import ObjectId
from src.monogodb import mongodb_collection
from pandas import read_json, DataFrame, to_datetime

from .predict_catboost import make_predict

def reprocess_data(report_id: str):
    def function():
        report = mongodb_collection.find_one({"_id": ObjectId(report_id)})

        data = read_json(report["data"])
        ml_data = read_json(report["ml_data"])
        ml_data["Пеиод__Начало нед"] = to_datetime(ml_data["Пеиод__Начало нед"], unit="ms")
        mean_std_info = report["mean_std_info"]
        columns_with_not_enough_information = report["excluded_columns"]

        predicted_data, shap_values, val_data = make_predict(ml_data, mean_std_info)

        mongodb_collection.update_one({"_id": ObjectId(report_id)}, {"$set": {
            "status": "ready",
            "data": data.to_json(),
            "shap_values": DataFrame(shap_values).to_json(),
            "val_values": val_data.to_json(),
            "predicted_data": predicted_data.to_json(),
            "ml_data": DataFrame(ml_data).to_json(),
            "excluded_columns": columns_with_not_enough_information,
            "mean_std_info": mean_std_info
        }})

    return function
