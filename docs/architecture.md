# Architecture Diagram

```mermaid
flowchart LR
    A[(PostgreSQL Loan Tables)] --> B[Conditional Data Extraction]
    B --> C[Data Sanity Checks]
    C --> D[Feature Engineering + Preprocessing]
    D --> E[Candidate Model Training]
    E --> F[Champion Model Selection]
    F --> G[Deployment Report]
    D --> H[Reference vs Current Dataset]
    H --> I[Data Drift Checks]
    F --> J[Model Drift / Performance Checks]
    I --> K{Retrain?}
    J --> K
    K -->|Yes| E
    K -->|No| L[Keep Champion]
    K --> M[Slack Alert]
    subgraph Orchestration
        N[Airflow DAG]
    end
    N --> B
    N --> C
    N --> D
    N --> E
    N --> I
    N --> J
```

The architecture is designed around a controlled monitoring workflow: data is extracted from PostgreSQL by date window, checked for sanity, transformed using a reusable scikit-learn preprocessing pipeline, trained against candidate models, and monitored against a reference window for feature drift and retraining signals.
