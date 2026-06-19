# Data Dictionary

| Field | Description | Type | Monitoring Use |
|---|---|---:|---|
| loan_id | Unique loan application identifier | text | Identifier, excluded from model |
| customer_id | Unique customer identifier | text | Identifier, excluded from model |
| loan_status | Historical loan decision label: `loan given` or `loan refused` | categorical | Target variable |
| application_time | Loan application timestamp | datetime | Batch extraction and time-window monitoring |
| current_loan_amount | Requested loan amount | numeric | Model feature and drift feature |
| term | Loan term category | categorical | Model feature and drift feature |
| credit_score | Borrower credit score | numeric | Model feature and drift feature |
| monthly_debt | Borrower monthly debt obligation | numeric | Model feature and engineered ratio input |
| annual_income | Borrower annual income | numeric | Model feature and engineered ratio input |
| years_of_credit_history | Credit history length | numeric | Model feature |
| months_since_last_delinquent | Recency of delinquency | numeric | Model feature |
| no_of_open_accounts | Open credit account count | numeric | Model feature |
| no_of_credit_problems | Number of credit problems | numeric | Model feature |
| current_credit_balance | Current credit balance | numeric | Model feature and utilization input |
| max_open_credit | Maximum open credit | numeric | Model feature and utilization input |
| bankruptcies | Bankruptcy count | numeric | Model feature |
| tax_liens | Tax lien count | numeric | Model feature |
| purpose | Loan purpose | categorical | Model feature and drift feature |
| home_ownership | Home ownership category | categorical | Model feature and drift feature |
