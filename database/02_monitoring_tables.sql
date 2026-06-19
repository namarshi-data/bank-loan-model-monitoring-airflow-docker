CREATE TABLE IF NOT EXISTS monitoring_runs (
    run_id TEXT PRIMARY KEY,
    run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reference_start DATE,
    reference_end DATE,
    current_start DATE,
    current_end DATE,
    champion_model TEXT,
    champion_metric TEXT,
    champion_metric_value DOUBLE PRECISION,
    retrain_recommended BOOLEAN,
    alert_level TEXT,
    notes TEXT
);
