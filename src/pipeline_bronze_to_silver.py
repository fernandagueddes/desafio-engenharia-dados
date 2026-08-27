from datetime import datetime
import os

import pandas as pd

from airflow import DAG
from airflow.operators.python import PythonOperator


# Paths inside the Airflow container
BASE_PATH = "/opt/airflow/data"
BRONZE_PATH = os.path.join(BASE_PATH, "bronze")
SILVER_PATH = os.path.join(BASE_PATH, "silver")

RAW_FILE = os.path.join(BRONZE_PATH, "raw_data.csv")
SILVER_FILE = os.path.join(SILVER_PATH, "usuarios_limpos.csv")


def calculate_age(date_of_birth: pd.Series) -> pd.Series:
    """
    Calculate age based on date of birth.
    """
    today = pd.Timestamp.today().normalize()

    age = today.year - date_of_birth.dt.year

    birthday_not_reached = (
        (date_of_birth.dt.month > today.month)
        | (
            (date_of_birth.dt.month == today.month)
            & (date_of_birth.dt.day > today.day)
        )
    )

    return age - birthday_not_reached.astype(int)


def bronze_to_silver():
    """
    Read raw data from the Bronze layer,
    clean and validate it, and save the result
    in the Silver layer.
    """

    # Validate input file
    if not os.path.exists(RAW_FILE):
        raise FileNotFoundError(
            f"Raw data file not found: {RAW_FILE}"
        )

    # Read raw data
    df = pd.read_csv(RAW_FILE)

    # Validate required columns
    required_columns = [
        "name",
        "email",
        "date_of_birth",
        "subscription_status",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Remove rows with missing critical values
    df = df.dropna(
        subset=[
            "name",
            "email",
            "date_of_birth",
        ]
    )

    # Validate email format
    df = df[
        df["email"]
        .astype(str)
        .str.contains("@", na=False)
    ].copy()

    # Convert date of birth
    df["date_of_birth"] = pd.to_datetime(
        df["date_of_birth"],
        errors="coerce",
    )

    # Remove invalid dates
    df = df.dropna(
        subset=["date_of_birth"]
    ).copy()

    # Calculate age
    df["age"] = calculate_age(
        df["date_of_birth"]
    )

    # Normalize subscription status
    df["status"] = (
        df["subscription_status"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # Create Silver directory if necessary
    os.makedirs(
        SILVER_PATH,
        exist_ok=True,
    )

    # Save cleaned data
    df.to_csv(
        SILVER_FILE,
        index=False,
    )

    print(
        f"Silver layer created successfully: "
        f"{SILVER_FILE} | Rows: {len(df)}"
    )


with DAG(
    dag_id="bronze_to_silver",
    description=(
        "Clean and transform raw Bronze data "
        "into the Silver layer"
    ),
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["etl", "bronze", "silver"],
) as dag:

    process_bronze_to_silver = PythonOperator(
        task_id="process_bronze_to_silver",
        python_callable=bronze_to_silver,
    )

