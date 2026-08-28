# ETL Data Pipeline with Apache Airflow

An end-to-end ETL data pipeline built with **Python, Apache Airflow, Pandas, and Docker**, following a **Bronze, Silver, and Gold layered architecture**.

The project demonstrates how raw data can be validated, cleaned, transformed, and aggregated through orchestrated data pipelines to produce analytics-ready datasets.

## Architecture

```text
Raw CSV Data
     │
     ▼
┌─────────────┐
│   BRONZE    │
│  Raw Data   │
└──────┬──────┘
       │
       │ Airflow
       ▼
┌─────────────┐
│   SILVER    │
│ Clean Data  │
└──────┬──────┘
       │
       │ Airflow
       ▼
┌─────────────┐
│    GOLD     │
│ Aggregated  │
│    Data     │
└─────────────┘
```

## Pipeline Overview

The pipeline is divided into two main processing stages.

### Bronze → Silver

The `pipeline_bronze_to_silver.py` DAG processes the raw dataset and applies data quality and transformation rules.

Main operations:

- Validates the existence of the source file
- Validates required columns
- Removes records with missing critical values
- Filters invalid email addresses
- Converts date fields
- Calculates user age
- Normalizes subscription status
- Stores the cleaned dataset in the Silver layer

### Silver → Gold

The `pipeline_silver_to_gold.py` DAG transforms the cleaned dataset into an analytics-ready aggregated table.

Main operations:

- Validates the Silver dataset
- Validates required columns
- Normalizes subscription status
- Validates age values
- Creates age bands
- Aggregates users by age band and subscription status
- Stores the final dataset in the Gold layer

## Project Structure

```text
.
├── pipeline/
│   └── data/
│       ├── bronze/
│       │   └── raw_data.csv
│       ├── silver/
│       │   └── usuarios_limpos.csv
│       └── gold/
│           └── usuarios_por_faixa_status.csv
│
├── src/
│   ├── pipeline_bronze_to_silver.py
│   └── pipeline_silver_to_gold.py
│
├── .gitignore
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Technologies

- **Python** — data processing and pipeline logic
- **Pandas** — data cleaning, validation, transformation, and aggregation
- **Apache Airflow** — workflow orchestration
- **Docker** — containerized execution environment
- **PostgreSQL** — Airflow metadata database
- **Git & GitHub** — version control and project documentation

## Data Layers

| Layer | Purpose | Output |
|---|---|---|
| Bronze | Raw source data | `raw_data.csv` |
| Silver | Cleaned and validated data | `usuarios_limpos.csv` |
| Gold | Aggregated analytics-ready data | `usuarios_por_faixa_status.csv` |

## Running the Project

### Prerequisites

Make sure you have installed:

- Docker
- Docker Compose

### 1. Clone the repository

```bash
git clone https://github.com/fernandagueddes/airflow-etl-data-pipeline.git
cd airflow-etl-data-pipeline
```

### 2. Start the environment

```bash
docker compose up
```

The Docker environment starts:

- PostgreSQL
- Airflow initialization service
- Airflow webserver
- Airflow scheduler

### 3. Access Apache Airflow

Open:

```text
http://localhost:8081
```

Default credentials:

```text
Username: airflow
Password: airflow
```

### 4. Run the pipelines

In the Airflow interface, run the DAGs in the following order:

```text
bronze_to_silver
        ↓
silver_to_gold
```

The first DAG validates, cleans, and transforms the raw dataset into the Silver layer.

The second DAG aggregates the processed data and generates the Gold dataset.

## Data Flow

```text
raw_data.csv
      │
      ▼
Bronze Layer
      │
      ▼
Data Validation
Data Cleaning
Data Transformation
      │
      ▼
Silver Layer
usuarios_limpos.csv
      │
      ▼
Age Band Creation
Aggregation by Status
      │
      ▼
Gold Layer
usuarios_por_faixa_status.csv
```

## Skills Demonstrated

This project demonstrates practical experience with:

- ETL pipeline development
- Workflow orchestration with Apache Airflow
- Data cleaning and transformation with Pandas
- Data quality validation
- Bronze, Silver, and Gold data architecture
- Dockerized data environments
- PostgreSQL integration with Airflow
- Data aggregation for analytical consumption
- Git version control
