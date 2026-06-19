from __future__ import annotations

import math

import numpy as np
import pandas as pd
from scipy import stats


def population_stability_index(reference: pd.Series, current: pd.Series, bins: int = 10) -> float:
    reference_clean = pd.to_numeric(reference, errors="coerce").dropna()
    current_clean = pd.to_numeric(current, errors="coerce").dropna()
    if reference_clean.empty or current_clean.empty:
        return float("nan")

    quantiles = np.unique(np.quantile(reference_clean, np.linspace(0, 1, bins + 1)))
    if len(quantiles) < 3:
        return 0.0
    quantiles[0] = -np.inf
    quantiles[-1] = np.inf
    ref_counts, _ = np.histogram(reference_clean, bins=quantiles)
    cur_counts, _ = np.histogram(current_clean, bins=quantiles)
    if ref_counts.sum() == 0 or cur_counts.sum() == 0:
        return float("nan")
    ref_pct = np.where(ref_counts == 0, 0.0001, ref_counts / ref_counts.sum())
    cur_pct = np.where(cur_counts == 0, 0.0001, cur_counts / cur_counts.sum())
    return float(np.sum((cur_pct - ref_pct) * np.log(cur_pct / ref_pct)))


def numeric_drift(reference: pd.Series, current: pd.Series) -> dict:
    ref = pd.to_numeric(reference, errors="coerce").dropna()
    cur = pd.to_numeric(current, errors="coerce").dropna()
    if len(ref) < 2 or len(cur) < 2:
        return {"psi": float("nan"), "ks_statistic": float("nan"), "ks_pvalue": float("nan")}
    ks = stats.ks_2samp(ref, cur)
    return {
        "psi": population_stability_index(ref, cur),
        "ks_statistic": float(ks.statistic),
        "ks_pvalue": float(ks.pvalue),
    }


def categorical_drift(reference: pd.Series, current: pd.Series) -> dict:
    ref_counts = reference.fillna("__missing__").astype(str).value_counts()
    cur_counts = current.fillna("__missing__").astype(str).value_counts()
    categories = sorted(set(ref_counts.index) | set(cur_counts.index))
    observed = np.array([[ref_counts.get(cat, 0), cur_counts.get(cat, 0)] for cat in categories], dtype=float)
    if observed.sum() == 0 or observed.shape[0] < 2:
        return {"chi2_statistic": float("nan"), "pvalue": float("nan")}
    # Add a small continuity correction so rare categories present in only one window
    # do not make the contingency test fail.
    observed = observed + 0.5
    chi2, pvalue, _, _ = stats.chi2_contingency(observed)
    return {"chi2_statistic": float(chi2), "pvalue": float(pvalue)}


def build_drift_report(
    reference: pd.DataFrame,
    current: pd.DataFrame,
    numeric_features: list[str],
    categorical_features: list[str],
    psi_warning_threshold: float,
    psi_failure_threshold: float,
    ks_pvalue_threshold: float,
    categorical_pvalue_threshold: float,
) -> dict:
    feature_reports = []
    for feature in numeric_features:
        if feature in reference.columns and feature in current.columns:
            report = numeric_drift(reference[feature], current[feature])
            psi = report["psi"]
            if math.isnan(psi):
                status = "not_evaluated"
            elif psi >= psi_failure_threshold or report["ks_pvalue"] < ks_pvalue_threshold:
                status = "fail"
            elif psi >= psi_warning_threshold:
                status = "warn"
            else:
                status = "pass"
            feature_reports.append({"feature": feature, "type": "numeric", "status": status, **report})

    for feature in categorical_features:
        if feature in reference.columns and feature in current.columns:
            report = categorical_drift(reference[feature], current[feature])
            pvalue = report["pvalue"]
            status = "not_evaluated" if math.isnan(pvalue) else (
                "fail" if pvalue < categorical_pvalue_threshold else "pass"
            )
            feature_reports.append({"feature": feature, "type": "categorical", "status": status, **report})

    failed = [item for item in feature_reports if item["status"] == "fail"]
    warned = [item for item in feature_reports if item["status"] == "warn"]
    return {
        "summary": {
            "features_evaluated": len(feature_reports),
            "failed_features": len(failed),
            "warning_features": len(warned),
            "alert_level": "fail" if failed else ("warn" if warned else "pass"),
            "retrain_recommended": bool(failed),
        },
        "features": feature_reports,
    }


def compare_performance(reference_metrics: dict, current_metrics: dict, max_auc_drop: float, max_f1_drop: float) -> dict:
    auc_drop = reference_metrics.get("roc_auc", 0) - current_metrics.get("roc_auc", 0)
    f1_drop = reference_metrics.get("f1", 0) - current_metrics.get("f1", 0)
    status = "fail" if auc_drop > max_auc_drop or f1_drop > max_f1_drop else "pass"
    return {
        "status": status,
        "auc_drop": float(auc_drop),
        "f1_drop": float(f1_drop),
        "retrain_recommended": status == "fail",
    }
