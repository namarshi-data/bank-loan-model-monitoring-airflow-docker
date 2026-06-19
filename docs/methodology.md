# Methodology

## 1. Business Framing

The project is framed as a retail banking model monitoring workflow. The model predicts historical loan eligibility outcomes and the monitoring layer detects when the input data or model behaviour has changed enough to require review or retraining.

## 2. Data Extraction

The production-style path extracts loan applications from PostgreSQL using configurable date windows. A small sample CSV is included so reviewers can run the workflow without private data.

## 3. Data Sanity

Sanity checks cover row count, required columns, duplicate rate, target availability, and missingness. Failed checks should stop deployment and trigger a review.

## 4. Feature Engineering

Feature engineering is implemented in reusable Python modules, not only in notebooks. Engineered features include debt-to-income ratio, credit utilization ratio, application month/quarter, tenure bucket, and credit-history proxy variables.

## 5. Model Training

Random Forest and Gradient Boosting are trained using a shared preprocessing pipeline. The champion is selected by ROC-AUC, with precision, recall, F1, and balanced accuracy reported for business review.

## 6. Monitoring

The monitoring layer compares a reference data window against a current data window using PSI, Kolmogorov-Smirnov tests for numeric features, and chi-square tests for categorical features. The result is summarized into pass/warn/fail alerts and retraining recommendations.
