Pipeline ETL com Apache Airflow
Este projeto foi desenvolvido como parte de um desafio de Engenharia de Dados. O objetivo é simular um pipeline completo utilizando o Apache Airflow, aplicando as camadas Bronze, Silver e Gold no processamento de dados. A orquestração é feita em contêineres Docker.

## Objetivo do Projeto

O pipeline implementa as seguintes etapas:
Extração (Bronze): Leitura de dados brutos.
Transformação e limpeza (Silver): Tratamento dos dados.
Agregação (Gold): Preparação para consumo analítico.

A orquestração é feita com o **Apache Airflow**, executando os processos em contêineres Docker.


---

## Estrutura do Projeto

```
├── docker-compose.yml
├── requirements.txt
├── src/                # DAGs do Airflow
│   ├── pipeline_bronze_to_silver.py
│   ├── pipeline_silver_to_gold.py
│   └── pipeline_dnc.py
├── pipeline/           # logs (ignorados no repositório)
├── data/
│   ├── bronze/
│   │   └── raw_data.csv
│   ├── silver/
│   │   └── usuarios_limpos.csv
│   └── gold/
│       └── usuarios_por_faixa_status.csv
└── .gitignore
```


---

##  Tecnologias Utilizadas

- Python  
- Apache Airflow  
- Docker  
- Pandas  
- Linux/CLI  
- Git e GitHub  

---

##  Etapas da Pipeline

###  1. Bronze → Silver (`pipeline_bronze_to_silver.py`)
- Lê dados brutos do CSV;
- Normaliza e limpa campos;
- Salva em `data/silver/`.

###  2. Silver → Gold (`pipeline_silver_to_gold.py`)
- Agrupa os dados por faixas etárias e status;
- Gera tabela final em `data/gold/`.

---

##  Como Executar o Projeto

Pré-requisitos
Certifique-se de ter o Docker e o Docker Compose instalados.

Subir o ambiente com Docker e Airflow:

###  1. Subir o ambiente com Docker e Airflow:

docker-compose up

Acesse o Airflow em: http://localhost:8080
Login padrão:
Usuário: airflow
Senha: airflow

---

###  3. Ativar e rodar as DAGs manualmente.

| Camada | Descrição       | Arquivo                                   |
| ------ | --------------- | ----------------------------------------- |
| Bronze | Dados brutos    | `data/bronze/raw_data.csv`                |
| Silver | Dados limpos    | `data/silver/usuarios_limpos.csv`         |
| Gold   | Dados agregados | `data/gold/usuarios_por_faixa_status.csv` |








