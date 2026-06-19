from __future__ import annotations

import pandas as pd


def data_sanity_report(
    df: pd.DataFrame,
    target_column: str,
    required_columns: list[str],
    min_row_count: int,
    max_missing_rate: float,
    max_duplicate_rate: float,
) -> dict:
    missing_required = [column for column in required_columns if column not in df.columns]
    duplicate_rate = float(df.duplicated().mean()) if len(df) else 1.0
    missing_rate = float(df[required_columns].isna().mean().max()) if not missing_required else 1.0
    target_present = target_column in df.columns and df[target_column].notna().any()

    checks = {
        "row_count_check": len(df) >= min_row_count,
        "required_columns_check": len(missing_required) == 0,
        "max_missing_rate_check": missing_rate <= max_missing_rate,
        "duplicate_rate_check": duplicate_rate <= max_duplicate_rate,
        "target_available_check": target_present,
    }
    return {
        "passed": all(checks.values()),
        "row_count": int(len(df)),
        "missing_required_columns": missing_required,
        "max_missing_rate": missing_rate,
        "duplicate_rate": duplicate_rate,
        "checks": checks,
    }
