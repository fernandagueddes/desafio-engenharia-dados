from datetime import datetime
import os
import pandas as pd

from airflow import DAG
from airflow.operators.python import PythonOperator

# Caminhos dentro do container (mapeados no docker-compose)
BASE_PATH = "/opt/airflow/data"
BRONZE = os.path.join(BASE_PATH, "bronze")
SILVER = os.path.join(BASE_PATH, "silver")

RAW_FILE = os.path.join(BRONZE, "raw_data.csv")
SILVER_OUT = os.path.join(SILVER, "usuarios_limpos.csv")

def bronze_to_silver():
    # 1) conferir se o arquivo bruto existe
    if not os.path.exists(RAW_FILE):
        raise FileNotFoundError(f"Não achei {RAW_FILE}. Coloque o raw_data.csv em data/bronze/.")

    # 2) ler CSV
    df = pd.read_csv(RAW_FILE)

    # 3) validar colunas do seu arquivo
    # Ex.: id,name,email,date_of_birth,signup_date,subscription_status
    required = ["name", "email", "date_of_birth", "subscription_status"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Colunas obrigatórias ausentes: {missing}")

    # 4) remover nulos nas colunas críticas
    df = df.dropna(subset=["name", "email", "date_of_birth"])

    # 5) manter só emails com "@"
    df = df[df["email"].astype(str).str.contains("@", na=False)]

    # 6) calcular idade a partir de date_of_birth
    dob = pd.to_datetime(df["date_of_birth"], errors="coerce", infer_datetime_format=True)
    df = df[dob.notna()].copy()
    today = pd.Timestamp("today").normalize()
    df["age"] = ((today - dob[dob.notna()]).dt.days // 365).astype(int)

    # 7) normalizar status
    df["status"] = df["subscription_status"].astype(str).str.strip().str.lower()

    # 8) garantir pasta e salvar
    os.makedirs(SILVER, exist_ok=True)
    df.to_csv(SILVER_OUT, index=False)
    print(f"OK: gerado {SILVER_OUT} com {len(df)} linhas.")

with DAG(
    dag_id="bronze_to_silver",
    description="Limpa dados brutos e gera usuarios_limpos.csv na camada silver",
    start_date=datetime(2025, 1, 1),
    schedule=None,   # execução manual
    catchup=False,
    tags=["dnc", "bronze", "silver"],
) as dag:
    task_bronze_to_silver = PythonOperator(
        task_id="process_bronze_to_silver",
        python_callable=bronze_to_silver,
    )

    task_bronze_to_silver

