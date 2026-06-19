from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from ml_monitoring.config import ProjectConfig
from ml_monitoring.features.preprocessing import build_preprocessor, split_features_target
from ml_monitoring.models.evaluate import choose_best_model, classification_metrics


def candidate_models(random_state: int) -> dict[str, object]:
    return {
        "random_forest": RandomForestClassifier(
            n_estimators=250,
            max_depth=10,
            min_samples_leaf=10,
            class_weight="balanced",
            random_state=random_state,
            n_jobs=-1,
        ),
        "gradient_boosting": GradientBoostingClassifier(random_state=random_state),
    }


def train_candidates(df: pd.DataFrame, config: ProjectConfig) -> dict:
    modeling = config.raw["modeling"]
    X, y = split_features_target(df, config)
    stratify = y if y.nunique() == 2 else None
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=float(modeling["test_size"]),
        random_state=int(modeling["random_state"]),
        stratify=stratify,
    )

    results: list[dict] = []
    trained: dict[str, Pipeline] = {}
    for name, estimator in candidate_models(int(modeling["random_state"])).items():
        pipeline = Pipeline(
            steps=[
                ("preprocessor", build_preprocessor(config)),
                ("model", estimator),
            ]
        )
        pipeline.fit(X_train, y_train)
        probabilities = pipeline.predict_proba(X_test)[:, 1]
        metrics = classification_metrics(
            y_true=y_test,
            y_probability=probabilities,
            threshold=float(modeling["approval_threshold"]),
        )
        results.append({"model_name": name, "metrics": metrics})
        trained[name] = pipeline

    best = choose_best_model(results, metric=modeling["champion_metric"])
    champion_model = trained[best["model_name"]]
    config.model_dir.mkdir(parents=True, exist_ok=True)
    model_path = config.model_dir / "champion_model.joblib"
    joblib.dump(champion_model, model_path)

    return {
        "champion_model_name": best["model_name"],
        "champion_model_path": str(model_path),
        "candidate_results": results,
        "champion_metrics": best["metrics"],
        "test_row_count": int(len(y_test)),
        "train_row_count": int(len(y_train)),
    }


def load_champion(model_path: str | Path):
    return joblib.load(model_path)
