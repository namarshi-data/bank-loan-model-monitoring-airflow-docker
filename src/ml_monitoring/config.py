from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class ProjectConfig:
    raw: dict[str, Any]
    path: Path

    @property
    def project_root(self) -> Path:
        return self.path.parent.parent.resolve()

    @property
    def target_column(self) -> str:
        return self.raw["data"]["target_column"]

    @property
    def positive_label(self) -> str:
        return self.raw["data"]["positive_label"]

    @property
    def date_column(self) -> str:
        return self.raw["data"]["date_column"]

    @property
    def numeric_features(self) -> list[str]:
        return list(self.raw["features"]["numeric"])

    @property
    def categorical_features(self) -> list[str]:
        return list(self.raw["features"]["categorical"])

    @property
    def model_dir(self) -> Path:
        return self.project_root / self.raw["outputs"]["model_dir"]

    @property
    def report_dir(self) -> Path:
        return self.project_root / self.raw["outputs"]["report_dir"]


def load_config(path: str | Path = "config/pipeline_config.yaml") -> ProjectConfig:
    config_path = Path(path)
    if not config_path.is_absolute():
        config_path = Path.cwd() / config_path
    with config_path.open("r", encoding="utf-8") as file:
        raw = yaml.safe_load(file)
    return ProjectConfig(raw=raw, path=config_path)
