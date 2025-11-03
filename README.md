# Big_data_and_cloud_project_de24

## Project Overview

This project is part of the Big Data & Cloud module in the YH Data Engineering program (STI, Stockholm).
It demonstrates how to deploy a data warehouse pipeline to Azure, automate data ingestion from JobTech API, and visualize HR analytics insights through an interactive Streamlit dashboard.

🧩 Objectives
 - Cloud Deployment:
Deploy an end-to-end data engineering pipeline (DLT → DBT → Dagster → Streamlit) on Azure using DuckDB as the data warehouse.

- Cost Estimation:
Estimate and monitor Azure costs using Azure Cost Management + Billing.



## Tools & Technologies

🐍 Python 3.11+

🦆 DuckDB

🧱 DLT (Data Loading Tool)

🧮 DBT (Data Build Tool)

⚙️ Dagster (orchestration)

🌐 Streamlit (dashboard)

☁️ Microsoft Azure (deployment)

🧾 Azure Cost Management + Billing (monitoring)


🧰 Project Structure

big_data_and_cloud_project_de24/
│
├── dlt_code/                  # Data extraction & load logic (JobTech API)
├── dbt_code/                  # dbt models, seeds, macros
├── dagster_code/              # Orchestration logic
├── dashboard/                 # Streamlit dashboard
├── duckdb_warehouse/          # DuckDB local data warehouse
├── docker/                    # Dockerfiles for each service
├── .env                       # Environment variables (API keys, paths)
├── requirements.txt            # Python dependencies
└── README.md                  # Project documentation




🚀 Deployment 

Step 1: Local Setup

git clone https://github.com/AndresTrujillo1811-bit/big_data_and_cloud_project_de24.git
cd big_data_and_cloud_project_de24
python -m venv .venv
source .venv/bin/activate      # or .venv\Scripts\activate (Windows)
pip install -r requirements.txt


Step 2: Run Locally
# Extract and load job ads
python dlt_code/load_job_ads.py

# Transform with dbt
cd dbt_code
dbt run

# Launch dashboard
streamlit run dashboard/dashboard_main.py



#### Step 3: Azure Cloud Deployment

 - Containerize all modules using Docker.

 - Push to Azure Container Registry (ACR).
 - Deploy on Azure App Service.


 ### Set up daily refresh (DuckDB update):

- Use Azure Container Instances or Azure Logic Apps to trigger daily dbt run.


##  💰 Cost Estimation & Budget Management

 Step 1: Set up Cost Management

# Example: Create a budget using Azure CLI
az consumption budget create \
  --amount 30 \
  --time-grain Monthly \
  --name HRAnalyticsBudget \
  --category cost \
  --scope /subscriptions/<subscription_id> \
  --start-date 2025-11-01 \
  --end-date 2026-11-01 \
  --notifications "{
      \"Actual_GreaterThan_80_Percent\": {
        \"enabled\": true,
        \"operator\": \"GreaterThan\",
        \"threshold\": 80,
        \"contactEmails\": [\".......\"]
      }
  }"

- This sets a monthly cost limit of 30 USD and notifies the team when spending exceeds 80% of the budget.

 # Step 2: Estimated Costs (per month)

 | Azure Service        | Description              | Usage     | Est. Cost (USD)  |
| -------------------- | ------------------------ | --------- | ---------------- |
| App Service (B1)     | Host Streamlit dashboard | Always On | $15              |
| Container Registry   | Store Docker images      | 1 GB      | $2               |
| Storage Account      | Store logs/data backups  | 10 GB     | $3               |
| Container Instances  | Daily DLT/DBT run        | 1 h/day   | $5               |
| Network & Monitoring | Insights, metrics        | -         | $3               |
| **Total**            |                          |           | **~$28 / month** |


## Step 3: Snowflake Comparison  with DuckDB

| Feature     | DuckDB                   | Snowflake                         |
| ----------- | ------------------------ | --------------------------------- |
| Cost        | Free (local compute)     | Pay-per-use (warehouse + storage) |
| Scalability | Local only               | Auto-scaling compute              |
| Maintenance | Manual                   | Fully managed                     |
| Ideal for   | Small to medium datasets | Enterprise scale pipelines        |


   

👥 Team & Contributions

| Member                        | Role          | Contribution                             |
| ----------------------------- | ------------- | ---------------------------------------- |
| **Mohammad Nurul Hassan**     | Data Engineer | DLT + DBT + Deployment + Cost Estimation |
| **Andres Trujillo**           | Data Engineer | Dagster + Streamlit + Azure Integration  |             |


   



