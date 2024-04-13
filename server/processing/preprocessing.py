import json
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
from sklearn.preprocessing import StandardScaler

NEED_REPEATS_FOR_SEASON_FEATURE = 5
MAX_DEVIATION_FOR_SEASON_FEATURE = 3
REQUIRED_PERCENTAGE_OF_NON_MISSING_VALUES = 0.05


def get_renamed_columns(header_data: pd.DataFrame) -> list[str]:
    column_names = []
    previous_section_name = ""
    previous_subsection_name = ""

    for i, column in enumerate(header_data.columns):
        if not pd.isna(header_data[column][2]):
            previous_section_name = str(header_data[column][2]).replace("\n", "")
        if not pd.isna(header_data[column][3]):
            previous_subsection_name = str(header_data[column][3]).replace("\n", "")

        column_name = str(header_data[column][4]).replace("\n", "")
        column_names.append(
            f"{previous_section_name}_{previous_subsection_name}_{column_name}"
        )

    return column_names


def find_season_features(data: pd.DataFrame) -> dict[str, list[int]]:
    season_features = {}
    for i, column in enumerate(data.columns):
        column_missing_data = [0]

        # создаем массив в котором каждое число означает количество пропусков между двумя существующими ячейками
        for value in data[column].notnull().astype(float):
            if value == 1:
                column_missing_data.append(0)
            elif value == 0:
                column_missing_data[-1] += 1

        # Проверяем есть ли у нас повторы в получившихся массивах. Если они есть то фича - сезонная
        for start_value in range(len(column_missing_data)):
            temp_season_interval = [start_value]
            if column_missing_data[start_value] == 0:
                continue
            for end_value in range(start_value + 1, len(column_missing_data)):
                if (
                    abs(
                        column_missing_data[end_value]
                        - column_missing_data[start_value]
                    )
                    < MAX_DEVIATION_FOR_SEASON_FEATURE
                    and column_missing_data[end_value] != 0
                ):
                    temp_season_interval.append(end_value)
                elif len(temp_season_interval) >= NEED_REPEATS_FOR_SEASON_FEATURE:
                    season_features[column] = [
                        1 if column_missing_data[0] > 0 else 0,
                        column_missing_data[start_value]
                        + MAX_DEVIATION_FOR_SEASON_FEATURE,
                    ]
                    break
                else:
                    break

            # Сохраняем сезонные фичи в отдельный массив. 0 будет первым значением, если пропуски надо заполнять вперед.
            # 1 если назад. Вторым числом передаем лимит заполнения пропусков
            if len(temp_season_interval) >= NEED_REPEATS_FOR_SEASON_FEATURE:
                season_features[column] = [
                    1 if column_missing_data[0] > 0 else 0,
                    column_missing_data[start_value] + MAX_DEVIATION_FOR_SEASON_FEATURE,
                ]
                break

    return season_features


def fill_season_features(data: pd.DataFrame, season_features_data: dict) -> None:
    for key, value in season_features_data.items():
        if value[0] == 0:
            data[key].ffill(inplace=True, limit=value[1])
        else:
            data[key].bfill(inplace=True, limit=value[1])


def delete_bad_columns(data: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    return (
        data.loc[:, data.notna().mean() >= REQUIRED_PERCENTAGE_OF_NON_MISSING_VALUES],
        [
            i
            for i in data.columns
            if data[i].notna().mean() < REQUIRED_PERCENTAGE_OF_NON_MISSING_VALUES
        ],
    )


def scale_data(data: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, dict[str, float]]]:
    ml_data = data.copy()
    for i, column in enumerate(
        ml_data.select_dtypes(include=["datetime64[ns]"]).columns
    ):
        ml_data[f"day{i}"] = ml_data[column].map(lambda x: x.day)
        ml_data[f"month{i}"] = ml_data[column].map(lambda x: x.month)

    ml_timestamps = ml_data.select_dtypes(include=["datetime64[ns]"])
    ml_data = ml_data.select_dtypes(exclude=["datetime64[ns]"])

    ml_data_columns = ml_data.columns

    scaler = StandardScaler()
    scaler.fit(ml_data)

    mean_std_info = {}

    for i, column in enumerate(range(data.shape[1])):
        mean_std_info[column] = {"mean": scaler.mean_[i], "std": scaler.scale_[i]}

    ml_data = scaler.transform(ml_data)

    ml_data = pd.DataFrame(ml_data)
    ml_data.columns = ml_data_columns
    ml_data = pd.concat([ml_data, ml_timestamps], axis=1)

    return ml_data, mean_std_info


def preprocess(
    data: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, list[str], dict[str, dict[str, float]]]:
    season_features = find_season_features(data)
    fill_season_features(data, season_features)
    data, columns_with_not_enough_information = delete_bad_columns(data)

    ml_data, mean_std_info = scale_data(data)

    return data, ml_data, columns_with_not_enough_information, mean_std_info


def main(
    fileobject,
) -> tuple[pd.DataFrame, pd.DataFrame, list[str], dict[str, dict[str, float]]]:
    header_data = pd.read_excel(fileobject, nrows=5)
    data = pd.read_excel(fileobject, skiprows=5, na_values=["", 0.0, " ", "\t"])
    data.columns = get_renamed_columns(header_data)

    data, ml_data, columns_with_not_enough_information, mean_std_info = preprocess(data)

    return data, ml_data, columns_with_not_enough_information, mean_std_info


if __name__ == "__main__":
    viz_data, ml_data, bad_columns, mean_std_info = main(
        open("train/train.xlsx", mode="rb")
    )

    viz_data.to_csv("viz_data.csv", index=False)
    pd.DataFrame(ml_data).to_csv("ml_data.csv", index=False)

    with open("bad_columns.txt", mode="w", encoding="utf8") as f:
        f.write("\n".join(ml_data))

    with open("mean_std_info.json", mode="w", encoding="utf8") as f:
        json.dump(mean_std_info, f)
