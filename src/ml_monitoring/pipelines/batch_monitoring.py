from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from uuid import uuid4

from ml_monitoring.alerts.slack import send_slack_alert
from ml_monitoring.config import load_config
from ml_monitoring.data.extract import extract_window
from ml_monitoring.data.sanity import data_sanity_report
from ml_monitoring.features.preprocessing import engineer_features
from ml_monitoring.models.train import train_candidates
from ml_monitoring.monitoring.drift import build_drift_report
from ml_monitoring.reports.reporting import save_json_report, write_deployment_report


def run_pipeline(config_path: str, source: str = "sample", send_slack: bool = False) -> dict:
    config = load_config(config_path)
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S") + "_" + uuid4().hex[:8]

    data_cfg = config.raw["data"]
    ref_window = data_cfg["reference_window"]
    cur_window = data_cfg["current_window"]

    reference = extract_window(config, ref_window["start"], ref_window["end"], source=source)
    current = extract_window(config, cur_window["start"], cur_window["end"], source=source)

    required_columns = (
        data_cfg["identifier_columns"]
        + [config.date_column, config.target_column]
        + [col for col in config.raw["features"]["numeric"] if col in reference.columns]
    )
    monitoring_cfg = config.raw["monitoring"]
    sanity_reference = data_sanity_report(
        reference,
        target_column=config.target_column,
        required_columns=required_columns,
        min_row_count=int(monitoring_cfg["min_row_count"]),
        max_missing_rate=float(monitoring_cfg["max_missing_rate"]),
        max_duplicate_rate=float(monitoring_cfg["max_duplicate_rate"]),
    )
    sanity_current = data_sanity_report(
        current,
        target_column=config.target_column,
        required_columns=required_columns,
        min_row_count=int(monitoring_cfg["min_row_count"]),
        max_missing_rate=float(monitoring_cfg["max_missing_rate"]),
        max_duplicate_rate=float(monitoring_cfg["max_duplicate_rate"]),
    )

    training_report = train_candidates(reference, config)

    reference_features = engineer_features(reference, config)
    current_features = engineer_features(current, config)
    drift_report = build_drift_report(
        reference=reference_features,
        current=current_features,
        numeric_features=config.numeric_features,
        categorical_features=config.categorical_features,
        psi_warning_threshold=float(monitoring_cfg["psi_warning_threshold"]),
        psi_failure_threshold=float(monitoring_cfg["psi_failure_threshold"]),
        ks_pvalue_threshold=float(monitoring_cfg["ks_pvalue_threshold"]),
        categorical_pvalue_threshold=float(monitoring_cfg["categorical_pvalue_threshold"]),
    )

    report = {
        "run_id": run_id,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": source,
        "reference_window": ref_window,
        "current_window": cur_window,
        "sanity": {"reference": sanity_reference, "current": sanity_current},
        "training": training_report,
        "drift": drift_report,
        "responsible_use_note": config.raw["project"]["responsible_use_note"],
    }
    report_root = config.report_dir
    save_json_report(report, report_root / "drift" / f"{run_id}_monitoring_report.json")
    write_deployment_report(report, report_root / "model" / f"{run_id}_deployment_report.md")

    if send_slack:
        alert = drift_report["summary"]["alert_level"]
        send_slack_alert(
            f"Loan monitoring pipeline finished. run_id={run_id}, alert_level={alert}, retrain={drift_report['summary']['retrain_recommended']}"
        )
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the bank loan model monitoring pipeline.")
    parser.add_argument("--config", default="config/pipeline_config.yaml")
    parser.add_argument("--source", choices=["sample", "postgres"], default="sample")
    parser.add_argument("--send-slack", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = run_pipeline(args.config, source=args.source, send_slack=args.send_slack)
    print(json.dumps({"run_id": report["run_id"], "drift_summary": report["drift"]["summary"]}, indent=2))


if __name__ == "__main__":
    main()
