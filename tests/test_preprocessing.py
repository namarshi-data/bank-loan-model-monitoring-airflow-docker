from pathlib import Path

import pandas as pd

from ml_monitoring.config import load_config
from ml_monitoring.features.preprocessing import engineer_features, split_features_target


def test_feature_engineering_creates_monitoring_features():
    config = load_config(Path(__file__).resolve().parents[1] / "config" / "pipeline_config.yaml")
    df = pd.read_csv(Path(__file__).resolve().parents[1] / "data" / "sample" / "loan_applications_sample.csv")
    engineered = engineer_features(df.head(25), config)
    for column in ["debt_to_income_ratio", "credit_utilization_ratio", "application_month"]:
        assert column in engineered.columns


def test_split_features_target_returns_binary_target():
    config = load_config(Path(__file__).resolve().parents[1] / "config" / "pipeline_config.yaml")
    df = pd.read_csv(Path(__file__).resolve().parents[1] / "data" / "sample" / "loan_applications_sample.csv")
    X, y = split_features_target(df.head(100), config)
    assert set(y.unique()).issubset({0, 1})
    assert X.shape[0] == y.shape[0]
