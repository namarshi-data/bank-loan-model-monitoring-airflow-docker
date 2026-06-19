CREATE TABLE IF NOT EXISTS loan_applications (
    loan_id TEXT PRIMARY KEY,
    customer_id TEXT,
    loan_status TEXT,
    application_time TIMESTAMP,
    current_loan_amount DOUBLE PRECISION,
    term TEXT,
    tax_liens DOUBLE PRECISION,
    purpose TEXT,
    no_of_properties DOUBLE PRECISION,
    home_ownership TEXT,
    annual_income DOUBLE PRECISION,
    years_in_current_job DOUBLE PRECISION,
    months_since_last_delinquent DOUBLE PRECISION,
    no_of_cars DOUBLE PRECISION,
    no_of_children DOUBLE PRECISION,
    credit_score DOUBLE PRECISION,
    monthly_debt DOUBLE PRECISION,
    years_of_credit_history DOUBLE PRECISION,
    no_of_open_accounts DOUBLE PRECISION,
    no_of_credit_problems DOUBLE PRECISION,
    current_credit_balance DOUBLE PRECISION,
    max_open_credit DOUBLE PRECISION,
    bankruptcies DOUBLE PRECISION
);

CREATE INDEX IF NOT EXISTS idx_loan_applications_application_time
ON loan_applications (application_time);

CREATE INDEX IF NOT EXISTS idx_loan_applications_loan_status
ON loan_applications (loan_status);
