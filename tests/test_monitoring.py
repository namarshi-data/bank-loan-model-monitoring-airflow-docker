import pandas as pd

from ml_monitoring.monitoring.drift import build_drift_report, population_stability_index


def test_psi_is_non_negative():
    ref = pd.Series([1, 2, 3, 4, 5, 6, 7, 8])
    cur = pd.Series([1, 2, 3, 4, 6, 7, 8, 9])
    assert population_stability_index(ref, cur) >= 0


def test_drift_report_has_summary():
    reference = pd.DataFrame({"income": [1, 2, 3, 4, 5], "term": ["short", "short", "long", "short", "long"]})
    current = pd.DataFrame({"income": [1, 2, 30, 40, 50], "term": ["short", "long", "long", "long", "long"]})
    report = build_drift_report(
        reference=reference,
        current=current,
        numeric_features=["income"],
        categorical_features=["term"],
        psi_warning_threshold=0.1,
        psi_failure_threshold=0.25,
        ks_pvalue_threshold=0.05,
        categorical_pvalue_threshold=0.05,
    )
    assert "summary" in report
    assert report["summary"]["features_evaluated"] == 2
