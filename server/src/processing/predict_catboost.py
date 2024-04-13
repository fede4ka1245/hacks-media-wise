from sklearn.metrics import mean_absolute_percentage_error

import shap
import pandas as pd
import numpy as np
from sklearn.model_selection import (
    KFold,
    StratifiedKFold,
    TimeSeriesSplit,
    train_test_split,
)
from catboost import CatBoostClassifier, CatBoostRegressor, Pool
from prophet import Prophet

import warnings

warnings.filterwarnings("ignore")

TARGET = "1_KPI данные понедельно АлфаРМ_Продажи, рубли"


def make_predict(
    train_df: pd.DataFrame,
    mean_std_info: dict[str, dict[str, float]],
    n_splits=5,
    cat_features=[],
    number_of_important_features=20,
    weeks_need_to_be_predicted=28,
) -> tuple[pd.DataFrame, np.ndarray, pd.DataFrame]:
    small_df = train_df[~train_df[TARGET].isna()]

    timestamps_df = small_df.select_dtypes(include=["datetime64[ns]"])
    train_df = small_df.select_dtypes(exclude=["datetime64[ns]"])
    train_df.drop(
        columns=["1_KPI данные понедельно АлфаРМ_Продажи, упаковки"], inplace=True
    )

    for col in cat_features:
        train_df[col] = train_df[col].astype("category")

    X = train_df.drop(columns=[TARGET])
    y = train_df[TARGET]

    model = CatBoostRegressor(
        depth=5,
        iterations=3500,
        learning_rate=0.06,
        loss_function="MAPE",
        eval_metric="MAPE",
        custom_metric="MAPE",
        boosting_type="Ordered",
        # Главная фишка катбуста - работа с категориальными признаками
        cat_features=cat_features,
        # ignored_features = ignored_features,
        # Регуляризация и ускорение
        colsample_bylevel=0.098,
        subsample=0.95,
        l2_leaf_reg=9,
        min_data_in_leaf=243,
        max_bin=187,
        random_strength=1,
        # Параметры ускорения
        task_type="CPU",
        thread_count=-1,
        bootstrap_type="Bernoulli",
        # Важное!
        random_seed=7575,
        # auto_class_weights="SqrtBalanced",
        early_stopping_rounds=50,
    )

    clfs = train_regressor_model(X, y, n_splits, cat_features, model)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    explainer = shap.TreeExplainer(clfs[0])

    val_dataset = Pool(data=X_test, label=y_test, cat_features=cat_features)
    shap_values = explainer.shap_values(val_dataset)
    vals = np.abs(shap_values).mean(0)
    feature_importance = pd.DataFrame(
        list(zip(X_train.columns, vals)),
        columns=["col_name", "feature_importance_vals"],
    )
    feature_importance.sort_values(
        by=["feature_importance_vals"], ascending=False, inplace=True
    )

    feature_importance["feature_importance_vals"] = feature_importance[
        "feature_importance_vals"
    ].round(2)
    important_features = feature_importance.head(
        number_of_important_features
    ).col_name.values
    columns_to_predict = [TARGET] + list(important_features)

    predicts_df = pd.DataFrame()

    for column in timestamps_df.columns:
        predicts_df[column] = [
            timestamps_df.iloc[-1][column] + pd.Timedelta(days=7 * (i + 1))
            for i in range(weeks_need_to_be_predicted + 1)
        ]

    train_selected, test_selected = (
        small_df.iloc[:200].copy(),
        small_df.iloc[:200].copy(),
    )

    for i, column_name in enumerate(columns_to_predict):
        tmp_df = pd.DataFrame()
        tmp_df["ds"] = timestamps_df[timestamps_df.columns[0]]
        tmp_df["y"] = small_df[columns_to_predict[i]].fillna(0)

        model = Prophet().fit(tmp_df)

        tmp_df = pd.DataFrame()
        tmp_df["ds"] = predicts_df[timestamps_df.columns[0]]

        predicts_df[column_name] = model.predict(tmp_df)["yhat"]

    val_features = val_dataset.get_features()
    val_df = pd.DataFrame(val_features, columns=val_dataset.get_feature_names())
    return get_real_values(predicts_df, mean_std_info), shap_values, val_df


def get_real_values(df: pd.DataFrame, mean_std_info: dict[str, dict[str, float]]):
    df.drop(columns=["day0", "month0"], inplace=True)
    for column in df.select_dtypes(exclude=["datetime64[ns]"]).columns:
        df[column] = (
            df[column] * mean_std_info[column]["std"] + mean_std_info[column]["mean"]
        )
    return df


def train_regressor_model(X, y, n_splits, cat_features, model):
    clfs = []
    scores = []
    tscv = TimeSeriesSplit(n_splits=n_splits)

    for train_index, test_index in tscv.split(X):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

        clf = model.copy()

        clfs.append(clf)

        clf.fit(
            X_train,
            y_train,
            eval_set=(X_test, y_test),
            verbose=100,
            use_best_model=True,
            plot=False,
        )

        y_pred = clf.predict(X_test)
        score = mean_absolute_percentage_error(
            y_test, y_pred
        )  # np.mean(np.array(y_pred == y_test))
        scores.append(score)
        print(f"fold: MAPE score: {score}")

    assert len(clfs) == n_splits
    print(
        "====>>> mean MAPE: " + str(np.mean(scores, dtype="float32")) + " <<<====",
        np.std(scores).round(4),
        "\n",
    )
    return clfs
