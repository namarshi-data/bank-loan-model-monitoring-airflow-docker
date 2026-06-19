from __future__ import annotations

from pathlib import Path

import pandas as pd

from ml_monitoring.config import ProjectConfig
from ml_monitoring.database import get_engine, read_sql_window


def load_sample_data(config: ProjectConfig) -> pd.DataFrame:
    sample_path = config.project_root / config.raw["data"]["sample_csv"]
    df = pd.read_csv(sample_path, parse_dates=[config.date_column])
    return df.sort_values(config.date_column).reset_index(drop=True)


def extract_from_postgres(
    config: ProjectConfig,
    start_date: str,
    end_date: str,
    database_url: str | None = None,
) -> pd.DataFrame:
    engine = get_engine(database_url)
    return read_sql_window(
        engine=engine,
        table_name=config.raw["data"]["table_name"],
        date_column=config.date_column,
        start_date=start_date,
        end_date=end_date,
    )


def extract_window(
    config: ProjectConfig,
    start_date: str,
    end_date: str,
    source: str = "sample",
    database_url: str | None = None,
) -> pd.DataFrame:
    if source == "postgres":
        return extract_from_postgres(config, start_date, end_date, database_url)

    df = load_sample_data(config)
    mask = (df[config.date_column] >= pd.Timestamp(start_date)) & (
        df[config.date_column] <= pd.Timestamp(end_date)
    )
    return df.loc[mask].copy().reset_index(drop=True)


def persist_snapshot(df: pd.DataFrame, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path
