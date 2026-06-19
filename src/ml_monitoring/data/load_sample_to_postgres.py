from __future__ import annotations

from pathlib import Path

import pandas as pd

from ml_monitoring.config import load_config
from ml_monitoring.database import execute_sql_file, get_engine, write_dataframe


def main() -> None:
    config = load_config()
    engine = get_engine()
    schema_path = config.project_root / "database" / "01_create_schema.sql"
    execute_sql_file(engine, schema_path)
    sample_path = config.project_root / config.raw["data"]["sample_csv"]
    df = pd.read_csv(sample_path, parse_dates=[config.date_column])
    write_dataframe(df, engine, config.raw["data"]["table_name"], if_exists="replace")
    print(f"Loaded {len(df):,} rows into {config.raw['data']['table_name']}.")


if __name__ == "__main__":
    main()
