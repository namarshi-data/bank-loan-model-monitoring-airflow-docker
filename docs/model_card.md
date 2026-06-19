# Model Card

## Intended Use

This model is a portfolio demonstration of a banking ML monitoring pipeline. It is intended for analytics, model monitoring, and MLOps education. It is not intended to automate real lending decisions.

## Prediction Target

Binary classification of historical loan outcome: `loan given` vs `loan refused`.

## Key Risks

- Training data may not represent a real Canadian bank portfolio.
- Historical loan outcomes may include policy bias and operational decisions.
- Credit decisions require governance, fairness review, adverse-action explainability, and human oversight.
- Model drift signals should trigger review, not automatic production replacement.

## Monitoring Controls

- Data sanity checks before training.
- Numeric and categorical feature drift checks.
- Champion model comparison and deployment report.
- Slack alert hook for Airflow orchestration.
- No secrets or credentials committed to GitHub.
