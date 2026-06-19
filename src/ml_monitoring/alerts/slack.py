from __future__ import annotations

import os

import requests


def send_slack_alert(message: str, webhook_url: str | None = None) -> bool:
    url = webhook_url or os.getenv("SLACK_WEBHOOK_URL")
    if not url:
        print(f"[SLACK SKIPPED] {message}")
        return False
    response = requests.post(url, json={"text": message}, timeout=10)
    response.raise_for_status()
    return True
