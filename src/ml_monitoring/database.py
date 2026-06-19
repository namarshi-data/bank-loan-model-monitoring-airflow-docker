from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine


def get_engine(database_url: str | None = None) -> Engine:
    url = database_url or os.getenv("DATABASE_URL")
    if not url:
        raise ValueError("DATABASE_URL is not set. Use .env or Docker Compose environment variables.")
    return create_engine(url, pool_pre_ping=True)


def read_sql_window(
    engine: Engine,
    table_name: str,
    date_column: str,
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    query = text(
        f"""
        SELECT *
        FROM {table_name}
        WHERE {date_column} >= :start_date
          AND {date_column} <= :end_date
        ORDER BY {date_column}
        """
    )
    return pd.read_sql(query, engine, params={"start_date": start_date, "end_date": end_date})


def write_dataframe(df: pd.DataFrame, engine: Engine, table_name: str, if_exists: str = "append") -> None:
    df.to_sql(table_name, engine, if_exists=if_exists, index=False, method="multi", chunksize=1000)


def execute_sql_file(engine: Engine, sql_path: str | Path) -> None:
    sql = Path(sql_path).read_text(encoding="utf-8")
    with engine.begin() as connection:
        for statement in sql.split(";"):
            statement = statement.strip()
            if statement:
                connection.execute(text(statement))
