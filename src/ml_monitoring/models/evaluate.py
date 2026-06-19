from __future__ import annotations

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


def classification_metrics(y_true, y_probability, threshold: float = 0.5) -> dict[str, float]:
    y_pred = (np.asarray(y_probability) >= threshold).astype(int)
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "balanced_accuracy": balanced_accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
    }
    try:
        metrics["roc_auc"] = roc_auc_score(y_true, y_probability)
    except ValueError:
        metrics["roc_auc"] = float("nan")
    return {key: float(value) for key, value in metrics.items()}


def choose_best_model(results: list[dict], metric: str) -> dict:
    if not results:
        raise ValueError("No model results were supplied.")
    return max(results, key=lambda result: result["metrics"].get(metric, float("-inf")))
