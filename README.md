# 🚀 Pipeline de Ingestão de Dados com Docker, PostgreSQL e Great Expectations

## 📌 Visão Geral

Este projeto implementa um pipeline completo de engenharia de dados
utilizando:

-   🐳 Docker para containerização\
-   🐘 PostgreSQL como banco de dados\
-   🐍 Python para ETL (Extract, Transform, Load)\
-   📊 Great Expectations para qualidade de dados

O objetivo é ingerir dados de acidentes rodoviários a partir de um
arquivo CSV, validar a qualidade dos dados e armazená-los em um banco
relacional.

------------------------------------------------------------------------

## 🏗️ Arquitetura

\[ CSV (Raw Layer) \] → \[ Pipeline Python (ETL) \] → \[ Validação
(Great Expectations) \] → \[ PostgreSQL \] → \[ Data Docs \]

------------------------------------------------------------------------

## 📂 Estrutura do Projeto

pipeline-project/ │ ├── app/ │ ├── pipeline.py │ ├── gx_validation.py │
├── requirements.txt │ ├── data/ │ └── raw/ │ └── acidentes_rodovias.csv
│ ├── Dockerfile ├── docker-compose.yml ├── .dockerignore ├──
great_expectations/ └── README.md

------------------------------------------------------------------------

## ⚙️ Tecnologias Utilizadas

-   Docker
-   PostgreSQL
-   Python 3.11
-   Pandas
-   SQLAlchemy
-   Great Expectations

------------------------------------------------------------------------

## 🐳 Como Executar

docker compose up --build

Para parar: docker compose down

Reset completo: docker compose down -v

------------------------------------------------------------------------

## 🐘 Banco de Dados

Host: postgres\
Porta: 5432\
Database: meubanco\
Usuário: admin\
Senha: admin123

------------------------------------------------------------------------

## 🐍 Pipeline

Etapas:

1.  Extract → leitura do CSV\
2.  Transform → limpeza e padronização\
3.  Load → carga no PostgreSQL

------------------------------------------------------------------------

## 📊 Qualidade de Dados

Validações com Great Expectations:

-   Not Null\
-   Range\
-   Formato de Data\
-   Unicidade\
-   Valores válidos

------------------------------------------------------------------------

## 📄 Data Docs

Gerar relatório:

python gx_validation.py

Local: great_expectations/uncommitted/data_docs/local_site/index.html

------------------------------------------------------------------------

## ⚠️ Problemas Comuns

Arquivo não encontrado → verificar /data/raw\
Erro Docker → remover container antigo\
Erro NumPy → usar wheel (--only-binary)

------------------------------------------------------------------------

## 🚀 Melhorias Futuras

-   Airflow\
-   Data Warehouse\
-   Dashboard\
-   Cloud

------------------------------------------------------------------------

## 📌 Conclusão

Projeto completo de engenharia de dados com ETL, validação e
persistência.
