from __future__ import annotations

import re

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from ml_monitoring.config import ProjectConfig


def _job_tenure_years(value: object) -> float:
    if pd.isna(value):
        return np.nan
    if isinstance(value, (int, float, np.integer, np.floating)):
        return float(value)
    text = str(value).lower().strip()
    if text in {"", "nan", "none"}:
        return np.nan
    if "<" in text:
        return 0.5
    if "10+" in text or "10 +" in text:
        return 10.0
    match = re.search(r"\d+(?:\.\d+)?", text)
    return float(match.group()) if match else np.nan


def _job_tenure_bucket(value: object) -> str:
    years = _job_tenure_years(value)
    if pd.isna(years):
        return "unknown"
    if years < 1:
        return "0_to_1"
    if years < 3:
        return "1_to_3"
    if years < 6:
        return "3_to_6"
    if years < 10:
        return "6_to_10"
    return "10_plus"


def engineer_features(df: pd.DataFrame, config: ProjectConfig) -> pd.DataFrame:
    output = df.copy()
    output[config.date_column] = pd.to_datetime(output[config.date_column], errors="coerce")
    tenure = output.get("years_in_current_job", pd.Series(index=output.index, dtype="float64"))
    output["years_in_current_job_numeric"] = tenure.map(_job_tenure_years)
    output["years_in_current_job_bucket"] = tenure.map(_job_tenure_bucket)

    output["debt_to_income_ratio"] = output["monthly_debt"] * 12 / output["annual_income"].replace(0, np.nan)
    output["credit_utilization_ratio"] = output["current_credit_balance"] / output[
        "max_open_credit"
    ].replace(0, np.nan)
    output["credit_history_to_age_proxy"] = output["years_of_credit_history"] / (
        output["years_in_current_job_numeric"].fillna(0) + 1
    )
    output["application_month"] = output[config.date_column].dt.month
    output["application_quarter"] = output[config.date_column].dt.quarter

    for column in ["debt_to_income_ratio", "credit_utilization_ratio", "credit_history_to_age_proxy"]:
        output[column] = output[column].replace([np.inf, -np.inf], np.nan)
    return output


def make_target(df: pd.DataFrame, config: ProjectConfig) -> pd.Series:
    return df[config.target_column].astype(str).str.lower().eq(config.positive_label.lower()).astype(int)


def build_preprocessor(config: ProjectConfig) -> ColumnTransformer:
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )
    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, config.numeric_features),
            ("categorical", categorical_pipeline, config.categorical_features),
        ],
        remainder="drop",
    )


def split_features_target(df: pd.DataFrame, config: ProjectConfig) -> tuple[pd.DataFrame, pd.Series]:
    features = engineer_features(df, config)
    y = make_target(features, config)
    feature_columns = config.numeric_features + config.categorical_features
    return features[feature_columns], y
