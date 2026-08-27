from datetime import datetime
from pathlib import Path

import pandas as pd

from airflow import DAG
from airflow.operators.python import PythonOperator


# Paths inside the Airflow container
DATA_DIR = Path("/opt/airflow/data")

SILVER_FILE = DATA_DIR / "silver" / "usuarios_limpos.csv"
GOLD_FILE = DATA_DIR / "gold" / "usuarios_por_faixa_status.csv"


def silver_to_gold():
    """
    Read cleaned data from the Silver layer,
    aggregate users by age band and status,
    and save the result in the Gold layer.
    """

    # Validate input file
    if not SILVER_FILE.exists():
        raise FileNotFoundError(
            f"Silver data file not found: {SILVER_FILE}"
        )

    # Read Silver data
    df = pd.read_csv(SILVER_FILE)

    # Validate required columns
    required_columns = ["age", "status"]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Normalize status
    df["status"] = (
        df["status"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # Keep only expected status values
    df["status"] = df["status"].where(
        df["status"].isin(["active", "inactive"]),
        "inactive",
    )

    # Convert age to numeric
    df["age"] = pd.to_numeric(
        df["age"],
        errors="coerce",
    )

    # Remove invalid ages
    df = df.dropna(subset=["age"]).copy()
    df = df[df["age"] >= 0].copy()

    # Create age bands
    bins = [
        -1,
        10,
        20,
        30,
        40,
        50,
        60,
        70,
        80,
        90,
        100,
        float("inf"),
    ]

    labels = [
        "0-10",
        "11-20",
        "21-30",
        "31-40",
        "41-50",
        "51-60",
        "61-70",
        "71-80",
        "81-90",
        "91-100",
        "101+",
    ]

    df["age_band"] = pd.cut(
        df["age"],
        bins=bins,
        labels=labels,
    )

    # Aggregate users by age band and status
    aggregated_df = (
        df.groupby(
            ["age_band", "status"],
            observed=False,
        )
        .size()
        .reset_index(name="user_count")
        .sort_values(
            ["age_band", "status"]
        )
    )

    # Create Gold directory if necessary
    GOLD_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Save aggregated data
    aggregated_df.to_csv(
        GOLD_FILE,
        index=False,
    )

    print(
        f"Gold layer created successfully: "
        f"{GOLD_FILE} | Rows: {len(aggregated_df)}"
    )


with DAG(
    dag_id="silver_to_gold",
    description=(
        "Aggregate Silver data by age band "
        "and subscription status"
    ),
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["etl", "silver", "gold"],
) as dag:

    process_silver_to_gold = PythonOperator(
        task_id="process_silver_to_gold",
        python_callable=silver_to_gold,
    )
