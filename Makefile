.PHONY: install test lint load-sample run-local up down

install:
	python -m pip install -e ".[dev]"

test:
	python -m pytest

lint:
	python -m ruff check src tests airflow/dags

load-sample:
	python scripts/load_sample_to_postgres.py

run-local:
	python scripts/run_local_monitoring.py --config config/pipeline_config.yaml

up:
	docker compose up -d --build

down:
	docker compose down --remove-orphans
