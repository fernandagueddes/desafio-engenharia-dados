Pipeline ETL com Apache Airflow

Este projeto foi desenvolvido como parte de um desafio de Engenharia de Dados. O objetivo é construir um pipeline completo utilizando o Apache Airflow, simulando as camadas Bronze, Silver e Gold no processamento de dados.

## Objetivo do Projeto

Implementar um pipeline que:
1. **Extrai** dados brutos (camada Bronze);
2. **Transforma e limpa** (camada Silver);
3. **Agrega e trata** os dados para consumo analítico (camada Gold).

A orquestração é feita com o **Apache Airflow**, executando os processos em contêineres Docker.

---

## Estrutura do Projeto

├── docker-compose.yml
├── requirements.txt
├── src/ # DAGs do Airflow
│ ├── pipeline_bronze_to_silver.py
│ ├── pipeline_silver_to_gold.py
│ └── pipeline_dnc.py
├── pipeline/ # logs (ignorados no repositório)
├── data/
│ ├── bronze/
│ │ └── raw_data.csv
│ ├── silver/
│ │ └── usuarios_limpos.csv
│ └── gold/
│ └── usuarios_por_faixa_status.csv
└── .gitignore


---

## ✅ Tecnologias Utilizadas

- Python  
- Apache Airflow  
- Docker  
- Pandas  
- Linux/CLI  
- Git e GitHub  

---

##  Etapas da Pipeline

### 🔹 1. Bronze → Silver (`pipeline_bronze_to_silver.py`)
- Lê dados brutos do CSV;
- Normaliza e limpa campos;
- Salva em `data/silver/`.

### 🔹 2. Silver → Gold (`pipeline_silver_to_gold.py`)
- Agrupa os dados por faixas etárias e status;
- Gera tabela final em `data/gold/`.

---

##  Como Executar o Projeto

### ✔️ 1. Subir o ambiente com Docker e Airflow:

```bash
docker-compose up

http://localhost:8080

Login padrão:
Usuário: airflow
Senha: airflow

✔️ 3. Ativar e rodar as DAGs manualmente.

| Camada | Descrição       | Arquivo                                   |
| ------ | --------------- | ----------------------------------------- |
| Bronze | Dados brutos    | `data/bronze/raw_data.csv`                |
| Silver | Dados limpos    | `data/silver/usuarios_limpos.csv`         |
| Gold   | Dados agregados | `data/gold/usuarios_por_faixa_status.csv` |








