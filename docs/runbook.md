# Runbook

## Local Python Run

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
python scripts/run_local_monitoring.py --config config/pipeline_config.yaml --source sample
```

## Docker + Airflow Run

```bash
cp .env.example .env
docker compose up -d --build
```

Open Airflow at `localhost:8080` using `admin` / `admin`.

Before triggering the DAG with PostgreSQL source, load the sample data into Postgres:

```bash
docker compose exec airflow-scheduler python /opt/airflow/project/scripts/load_sample_to_postgres.py
```

Then trigger the `bank_loan_model_monitoring` DAG.

## Expected Outputs

- `models/champion_model.joblib`
- `reports/model/*_deployment_report.md`
- `reports/drift/*_monitoring_report.json`
