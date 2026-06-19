from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def save_json_report(report: dict, path: str | Path) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    return output_path


def write_deployment_report(report: dict, path: str | Path) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    champion = report["training"]["champion_model_name"]
    metrics = report["training"]["champion_metrics"]
    drift = report["drift"]["summary"]
    lines = [
        "# Model Deployment and Monitoring Report",
        "",
        f"Generated at: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Champion Model",
        f"- Selected model: `{champion}`",
        f"- ROC-AUC: {metrics.get('roc_auc', float('nan')):.4f}",
        f"- F1: {metrics.get('f1', float('nan')):.4f}",
        f"- Precision: {metrics.get('precision', float('nan')):.4f}",
        f"- Recall: {metrics.get('recall', float('nan')):.4f}",
        "",
        "## Monitoring Decision",
        f"- Drift alert level: `{drift['alert_level']}`",
        f"- Failed features: {drift['failed_features']}",
        f"- Warning features: {drift['warning_features']}",
        f"- Retrain recommended: `{drift['retrain_recommended']}`",
        "",
        "## Responsible Use",
        "This model is documented as a decision-support workflow. It should not be used as the sole basis for automated credit approval or decline decisions.",
    ]
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path
