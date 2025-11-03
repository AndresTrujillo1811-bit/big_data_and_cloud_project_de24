# 🧠 Big Data & Cloud Project – HR Analytics Dashboard

## 🧭 Project Overview

This project is part of the **Big Data & Cloud** module in the **YH Data Engineering program (STI, Stockholm)**.  
It demonstrates how to **deploy a data warehouse pipeline to Azure**, automate data ingestion from **JobTech API**,  
and visualize HR analytics insights through an **interactive Streamlit dashboard**.

---

## 🧩 Objectives

- **Cloud Deployment:**  
  Deploy an end-to-end data engineering pipeline (**DLT → DBT → Dagster → Streamlit**) on **Azure** using **DuckDB** as the data warehouse.

- **Cost Estimation:**  
  Estimate and monitor **Azure costs** using **Azure Cost Management + Billing**.

---

## 🧰 Tools & Technologies

| Tool | Description |
|------|--------------|
| 🐍 **Python 3.11+** | Core programming language |
| 🦆 **DuckDB** | Analytical database engine |
| 🧱 **DLT (Data Loading Tool)** | Data extraction & loading |
| 🧮 **DBT (Data Build Tool)** | Data transformation & modeling |
| ⚙️ **Dagster** | Pipeline orchestration |
| 🌐 **Streamlit** | Dashboard visualization |
| ☁️ **Microsoft Azure** | Cloud deployment platform |
| 🧾 **Azure Cost Management + Billing** | Cost tracking and budgeting |

---

## 🧱 Project Structure

```bash
big_data_and_cloud_project_de24/
│
├── dlt_code/                  # Data extraction & load logic (JobTech API)
├── dbt_code/                  # dbt models, seeds, macros
├── dagster_code/              # Orchestration logic
├── dashboard/                 # Streamlit dashboard
├── duckdb_warehouse/          # DuckDB local data warehouse
├── docker/                    # Dockerfiles for each service
├── .env                       # Environment variables (API keys, paths)
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

---

## 🚀 Deployment Guide

### 🧩 Local Setup

```bash
# Clone the repository
git clone https://github.com/AndresTrujillo1811-bit/big_data_and_cloud_project_de24.git

# Navigate to project folder
cd big_data_and_cloud_project_de24

# Create a virtual environment
python -m venv .venv

# Activate environment
source .venv/bin/activate      # macOS/Linux
.venv\Scripts\activate       # Windows

# Install dependencies
pip install -r requirements.txt
```

---

### 🧩 Run Locally

```bash
# Extract and load job ads
python dlt_code/load_job_ads.py

# Transform with dbt
dbt run

# Launch dashboard
streamlit run dashboard/dashboard_main.py
```

---

## ☁️ Azure Cloud Deployment

- Containerize all modules using **Docker**.  
- Push Docker images to **Azure Container Registry (ACR)**.  
- Deploy Streamlit dashboard on **Azure App Service**.

### 🔁 Set up daily refresh (DuckDB update)

Use **Azure Container Instances** or **Azure Logic Apps** to trigger daily `dbt run`.

---

## 💰 Cost Estimation & Budget Management

### 🪙 Step 1: Set up Azure Cost Management

Follow [Microsoft’s official tutorial](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets?tabs=psbudget)  
to create and manage your budget.

```bash
# Create a budget using Azure CLI
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
        \"contactEmails\": [\"info@swedbd.nu\"]
      }
  }"
```

💡 This sets a **monthly cost limit of $30** and sends an **email alert when spending exceeds 80%** of the budget.

---

### 🧾 Step 2: Estimated Monthly Costs

| Azure Service        | Description              | Usage     | Est. Cost (USD) |
| -------------------- | ------------------------ | --------- | ---------------- |
| App Service (B1)     | Host Streamlit dashboard | Always On | $15 |
| Container Registry   | Store Docker images      | 1 GB | $2 |
| Storage Account      | Store logs/data backups  | 10 GB | $3 |
| Container Instances  | Daily DLT/DBT run        | 1 h/day | $5 |
| Network & Monitoring | Insights, metrics        | - | $3 |
| **Total** |  |  | **~$28 / month** |

---

### ❄️ Step 3: Snowflake vs DuckDB Comparison

| Feature     | DuckDB                   | Snowflake                         |
| ------------ | ------------------------ | --------------------------------- |
| Cost        | Free (local compute)     | Pay-per-use (warehouse + storage) |
| Scalability | Local only               | Auto-scaling compute              |
| Maintenance | Manual                   | Fully managed                     |
| Ideal for   | Small to medium datasets | Enterprise-scale pipelines        |

---

## 👥 Team & Contributions

| Member                    | Role          | Contribution |
| -------------------------- | ------------- | ------------- |
| **Mohammad Nurul Hassan** | Data Engineer | DLT + DBT + Deployment + Cost Estimation |
| **Andres Trujillo**       | Data Engineer | Dagster + Streamlit + Azure Integration  |

---
