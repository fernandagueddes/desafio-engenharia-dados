from datetime import datetime
from pathlib import Path
import pandas as pd

from airflow import DAG
from airflow.operators.python import PythonOperator

# Caminhos (host montado em /opt/airflow/data)
DATA_DIR = Path("/opt/airflow/data")
SILVER = DATA_DIR / "silver" / "usuarios_limpos.csv"
GOLD   = DATA_DIR / "gold"   / "usuarios_por_faixa_status.csv"

def silver_to_gold():
    # 1) Ler dados da Silver
    df = pd.read_csv(SILVER)

    # 2) Normalizar/garantir coluna de status (active/inactive)
    df["status"] = df["status"].astype(str).str.strip().str.lower()
    df["status"] = df["status"].where(df["status"].isin(["active", "inactive"]), "inactive")

    # 3) Criar faixas etárias de 0-10, 11-20, 21-30, ... até 100+
    bins = list(range(0, 101, 10)) + [200]   # 0..10..100 e um topo 200 pra capturar idades maiores
    labels = [f"{i}-{i+10}" for i in range(0, 100, 10)] + ["100+"]

    # Corrigido: usar "age" (não "idade")
    df["age_band"] = pd.cut(df["age"], bins=bins, right=True, include_lowest=True, labels=labels)

    # 4) Agregar: contagem por faixa etária e status
    agg = (
        df.groupby(["age_band", "status"])
          .size()
          .reset_index(name="qtd_usuarios")
          .sort_values(["age_band", "status"])
    )

    # 5) Garantir pasta gold e salvar CSV
    GOLD.parent.mkdir(parents=True, exist_ok=True)
    agg.to_csv(GOLD, index=False)

default_args = {
    "owner": "airflow",
}

with DAG(
    dag_id="silver_to_gold",
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
    tags=["dnc", "etl", "silver->gold"],
) as dag:

    process_silver_to_gold = PythonOperator(
        task_id="process_silver_to_gold",
        python_callable=silver_to_gold,
    )
