from __future__ import annotations

import pendulum
from airflow.decorators import dag, task

PROJECT_CONFIG = "/opt/airflow/project/config/pipeline_config.yaml"


@dag(
    dag_id="bank_loan_model_monitoring",
    start_date=pendulum.datetime(2026, 1, 1, tz="America/Toronto"),
    schedule="@daily",
    catchup=False,
    tags=["mlops", "banking", "model-monitoring", "drift"],
)
def bank_loan_model_monitoring():
    @task(task_id="run_monitoring_pipeline")
    def run_monitoring_pipeline() -> dict:
        from ml_monitoring.pipelines.batch_monitoring import run_pipeline

        report = run_pipeline(config_path=PROJECT_CONFIG, source="postgres", send_slack=True)
        return {
            "run_id": report["run_id"],
            "alert_level": report["drift"]["summary"]["alert_level"],
            "retrain_recommended": report["drift"]["summary"]["retrain_recommended"],
        }

    run_monitoring_pipeline()


bank_loan_model_monitoring()
