import pandas as pd

from ml_monitoring.data.sanity import data_sanity_report


def test_data_sanity_report_flags_required_columns():
    df = pd.DataFrame({"loan_status": ["loan given"], "income": [100]})
    report = data_sanity_report(
        df,
        target_column="loan_status",
        required_columns=["loan_status", "income", "missing_col"],
        min_row_count=1,
        max_missing_rate=0.5,
        max_duplicate_rate=0.1,
    )
    assert report["passed"] is False
    assert "missing_col" in report["missing_required_columns"]
