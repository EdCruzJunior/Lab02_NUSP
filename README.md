# 🚀 Pipeline de Engenharia de Dados com DBT + PostgreSQL + Apache Superset

## 📊 Visão Geral --

Este projeto demonstra a construção de um pipeline moderno de dados, transformando dados brutos em insights analíticos utilizando ferramentas amplamente utilizadas no mercado.

### 🎯 Objetivo
Transformar dados de acidentes (CSV) em uma camada analítica estruturada (GOLD) e disponibilizar insights através de dashboards interativos.

Este projeto implementa um pipeline completo de engenharia de dados:
CSV → PostgreSQL (RAW) → DBT (STAGING → MART/GOLD) → Apache Superset (Dashboard)

---

## 🧠 Storytelling

Empresas frequentemente possuem dados brutos (CSV, logs, APIs), mas enfrentam dificuldades em:

- Padronização de dados
- Governança e qualidade
- Transformação em insights

Este projeto resolve esses desafios através de um pipeline completo:

👉 **RAW → STAGING → GOLD → DASHBOARD**

---

## 🧭 Arquitetura do Pipeline

```text
            +------------------+
            |     CSV RAW      |
            +--------+---------+
                     |
                     v
            +------------------+
            |   PostgreSQL     |
            |   (RAW Layer)    |
            +--------+---------+
                     |
                     v
            +------------------+
            |       DBT        |
            | STAGING / MARTS  |
            +--------+---------+
                     |
                     v
            +------------------+
            | Apache Superset  |
            |   Dashboards     |
            +------------------+

```
---
## 🔄 Execução do Pipeline de Ingestão e Transformação

Antes da execução do DBT e da criação dos dashboards no Apache Superset, é necessário executar o pipeline de ingestão responsável por:

```text
📥 Realizar o download do arquivo RAW (acidentes_2026.csv)
🧹 Executar a limpeza e padronização dos dados
🏗️ Estruturar os dados para a camada analítica
🥇 Disponibilizar os dados tratados na camada GOLD utilizada pelo DBT e pelo Superset
🚀 Build e execução do pipeline
```
O pipeline está implementado no arquivo: pipeline.py
---
## ▶️ Executar o pipeline

```bash
python pipeline.py

```

## ⚙️ Responsabilidades do pipeline

O pipeline realiza automaticamente:
```text
Download do dataset RAW (acidentes_2026.csv)
Leitura e validação dos dados
Tratamento de valores inconsistentes
Padronização de colunas e tipos de dados
Carga no PostgreSQL (camada RAW)
Preparação da base para transformação via DBT
```

## 🧭 Fluxo completo de dados

```text
CSV RAW
   ↓
pipeline.py
   ↓
PostgreSQL (RAW)
   ↓
DBT (STAGING → GOLD)
   ↓
Apache Superset (Dashboard)
```

## 🎯 Objetivo da camada GOLD
A camada GOLD representa os dados consolidados e preparados para consumo analítico, permitindo:

```text
📊 Construção de dashboards
📈 Criação de KPIs
🔍 Exploração analítica
🧠 Geração de insights de negócio
```

## ⚠️ Importante

O DBT depende da existência dos dados carregados pelo pipeline.py.
Portanto, o pipeline deve ser executado antes dos comandos:

```bash
dbt run
dbt test
dbt docs generate
```
---

## 🐳 Ambiente (Docker Compose) --

📄 docker-compose.yml

```yaml
version: '3.9'

services:
  postgres:
    image: postgres:15
    container_name: postgres_lab02
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: admin123
      POSTGRES_DB: acidentes_db
    ports:
      - "5433:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - pipeline_network



  superset:
    image: apache/superset:latest-dev
    container_name: superset_dbt3
    ports:
    - "8092:8088"
    environment:
      SUPERSET_SECRET_KEY: "vztqIUXSrDrrWSrSKOkOh1vX9PJ7S9DhQ0DwL2PTcQt58vvOSCe4a6fx"
    depends_on:
    - postgres
    networks:
    - pipeline_network

  pipeline:
    build: .
    container_name: ingestion_pipeline_lab02
    depends_on:
      - postgres
    volumes:
      - ./data:/app/data
      - ./great_expectations:/app/great_expectations
    networks:
      - pipeline_network

volumes:
  postgres_data:

networks:
  pipeline_network:
    driver: bridge

```


---

## 🧱 1. Ambiente Python (DBT)

```bash
py -3.11 -m venv venv_dbt
venv_dbt\Scripts\activate
pip install --upgrade pip
pip install dbt-postgres
```
---

## 🐘 2. Subir PostgreSQL (Docker)

```bash
docker run -d \
  --name postgres_lab02 \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=admin123 \
  -e POSTGRES_DB=acidentes_db \
  -p 5433:5432 \
  postgres:15
```

---

## 📥 3. Criar tabela RAW

```sql
CREATE TABLE acidentes_raw (
    data DATE,
    hora TIME,
    concessionaria VARCHAR(50),
    rodovia VARCHAR(20),
    km NUMERIC(6,2),
    sentido VARCHAR(10),
    latitude NUMERIC(10,6),
    longitude NUMERIC(10,6),
    classe VARCHAR(100),
    subclasse VARCHAR(150),
    causa_provavel VARCHAR(255),
    vitima_ilesa INT,
    vitima_leve INT,
    vitima_moderada INT,
    vitima_grave INT,
    vitima_fatal INT,
    vitimas_sem_info INT,
    veiculos_envolvidos TEXT,
    visibilidade VARCHAR(50),
    condicao_meteriologica VARCHAR(50),
    municipio VARCHAR(100),
    regiao_administrativa VARCHAR(100),
    regional_der VARCHAR(50),
    jurisdicao VARCHAR(50)
);
```

---

## 📥 4. Importar CSV

```bash
docker cp acidentes_2026.csv postgres_lab02:/tmp/acidentes.csv
```

```sql
COPY acidentes_raw
FROM '/tmp/acidentes.csv'
DELIMITER ','
CSV HEADER
ENCODING 'LATIN1';
```

---

## 🏗️ 5. Inicializar DBT

```bash
dbt init lab02_dbt
cd lab02_dbt
```
---

## ⚙️ 6. Configurar profiles.yml

Path do arquivo profiles.yml: C:\Users\username\\.dbt\profiles.yml

```yaml
lab02_dbt:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost
      user: admin
      password: admin123
      port: 5433
      dbname: acidentes_db
      schema: public
```
---

## 📂 7. Estrutura do Projeto

```
models/
├── staging/
│   ├── sources.yml
│  
├── marts/
│   ├── schema.yml
├── dim_localidade.sql
├── fct_acidentes.sql
└── stg_acidentes.sql

macros/
└── classificar_gravidade.sql
tests/
├── schema.yml
├── test_data_futura.sql
└── test_vitima_negativa.sql
```

---
## 🔗 8. Sources
```text
📄 staging/sources.yml
```

```yaml
version: 2

sources:
  - name: raw
    schema: public
    tables:
      - name: acidentes_raw
```

---

## 🧱 9. Models

### 1. Staging
```text
📄 models/stg_acidentes.sql
```
```sql
select
    data,
    hora,
    municipio,
    estado,
    classe,
    subclasse,
    vitima_fatal,
    vitima_grave,
    vitima_leve,
    vitima_ilesa
from {{ source('raw', 'acidentes_raw') }}
```

### 2. Mart dimensão
```text
📄 models/dim_localidade.sql
```
```sql
select distinct
    municipio,
    regiao_administrativa,
    regional_der
from {{ ref('stg_acidentes') }}
```
### 3. Mart fato
```text
📄 models/fct_acidentes.sql
```
```sql
select
    data,
    municipio,
    classe,
    subclasse,
    vitima_fatal,
    vitima_grave,
    vitima_leve
from {{ ref('stg_acidentes') }}
```
### 3. Mart fato
```text
📄 models/fct_acidentes.sql
```
```sql
select
    data,
    municipio,
    classe,
    subclasse,
    vitima_fatal,
    vitima_grave,
    vitima_leve
from {{ ref('stg_acidentes') }}
```

---

## 🧩 10. Macro

```text
📄 macros/classificar_gravidade.sql
```
```sql
{% macro classificar_gravidade(col) %}
    case
        when {{ col }} >= 5 then 'ALTA'
        when {{ col }} >= 1 then 'MEDIA'
        else 'BAIXA'
    end
{% endmacro %}
```

---
## 🧪 10. Testes

## a. Testes Genéricos
```text
📄 marts/schema.yml
```

```yaml
version: 2

models:
  - name: fct_acidentes
    columns:
      - name: municipio
        tests:
          - not_null

      - name: data
        tests:
          - not_null

  - name: dim_localidade
    columns:
      - name: municipio
        tests:
          - unique
          - not_null
```
## b. Testes Singulares
```text
📄 tests/test_vitima_negativa.sql
```

```sql
select *
from {{ ref('fct_acidentes') }}
where vitima_fatal < 0
```

```text
📄 tests/test_data_futura.sql
```

```sql
select *
from {{ ref('fct_acidentes') }}
where data > current_date
```

---

## 📊 11. Documentação

Acessar o caminho do ambiente python 3.11 criado (Item 2 do documento): lab02_dbt e executar os comandos abaixo:

```bash
dbt docs generate
dbt docs serve
```
Abrir:

```bash
http://localhost:8080
```
<img width="919" height="422" alt="image" src="https://github.com/user-attachments/assets/212795b6-aef6-4dcb-a459-530e8479c0f9" />

---

## 🚀 Execução final

Acessar o caminho do ambiente python 3.11 criado (Item 1 do documento): lab02_dbt e executar os comandos abaixo:

```bash
dbt run
dbt test
dbt docs generate
dbt docs serve
```
---

## 🐳 12. Apache Superset

### Build (imagem customizada com driver PostgreSQL)
Criar um arquivo Dockerfile.superset e deixá-lo na raiz do projeto:

```dockerfile
FROM apache/superset:latest
USER root
RUN pip install psycopg[binary]
USER superset

```
### Subir Superset
```bash
docker run -d \
  --name superset_dbt3 \
  -p 8092:8088 \
  -e SUPERSET_SECRET_KEY="vztqIUXSrDrrWSrSKOkOh1vX9PJ7S9DhQ0DwL2PTcQt58vvOSCe4a6fx" \
  apache/superset 
```


### Inicializar Superset

```bash
docker exec -it superset_dbt3 superset db upgrade

docker exec -it superset_dbt3 superset fab create-admin \
  --username admin \
  --firstname Admin \
  --lastname User \
  --email admin@admin.com \
  --password admin

docker exec -it superset_dbt3 superset init
```

### Acessar Superset
```bash
http://localhost:8092
```

---

## 🔗 13. Conectar Superset ao PostgreSQL

```
postgresql://admin:admin123@ postgres_lab02:5433/acidentes_db
```

--

## 📈 14. Dashboard

Criar 3 gráficos:

- 📊 Barra → Acidentes por município
- 📉 Linha → Evolução no tempo
- 🧭 Scatter → Gravidade dos acidentes

<img width="962" height="400" alt="image" src="https://github.com/user-attachments/assets/a65aaa36-ce56-4ebb-a3f5-92ce7cfa63d5" />

---
## 📊 1. Criar Dataset no Superset

## 🧱 Passo 1

```text
No Superset:

👉 Data → Datasets → + Dataset
```

## 🧱 Passo 2

Preencher:
```text
Database → acidentes_db
Schema → public
Table → fct_acidentes

👉 Clique: Create Dataset
```

## 📊 2. VISUAL 1 — Gráfico de Barras

🎯 Objetivo:
Acidentes por município

## 🧱 Passos
 ```text
👉 Charts → + Chart
Dataset: fct_acidentes
Chart Type: Bar Chart
```

## ⚙️ Configuração 

```text
X Axis → municipio
Metric → COUNT(*)

Nome:
Acidentes por Município
```


## 📉 3. VISUAL 2 — Série Temporal

## 🎯 Objetivo:

Evolução dos acidentes no tempo

## 🧱 Passos

```text
👉 Novo Chart

Dataset: fct_acidentes
Tipo: Time-series Line Chart
```

## ⚙️ Configuração

```text
Time Column → data
Metric → COUNT(*)
Time Grain → Day

Evolução de Acidentes
```

### 🧭 4. VISUAL 3 — Dispersão (Scatter)

🎯 Objetivo:
Gravidade dos acidentes

## 🧱 Passos

``` text 
👉 Novo Chart

Tipo: Scatter Plot
⚙️ Configuração
X → vitima_fatal
Y → vitima_grave
Size → vitima_leve
```

Gravidade dos Acidentes


## 📊 5. Criar Dashboard

## 🧱 Passo 1

```text
👉 Dashboards → + Dashboard

Nome:
Dashboard Acidentes
```

## 🧱 Passo 2

```text
Clique:

👉 Edit Dashboard
```

## 🧱 Passo 3 — Adicionar gráficos

```text
Arraste:

Acidentes por Município
Evolução de Acidentes
Gravidade dos Acidentes

```
---

## 🎯 Resultado Final

✔ Pipeline completo funcionando  
✔ Camada GOLD pronta  
✔ Dashboard interativo  

---

## 🧱 Stack Tecnológica

```text
🐘 PostgreSQL (Banco de dados)
🔧 DBT (Transformação de dados)
📊 Apache Superset (Visualização)
🐳 Docker (Containerização)
🐍 Python 3.11 (Ambiente)
📥 Ingestão de Dados
Fonte: CSV de acidentes
Tabela RAW:
acidentes_raw

🔄 Modelagem DBT
🟡 Staging Layer
```

---

## Limpeza e padronização
Seleção de colunas relevantes

```text
🟢 Gold Layer (Marts)


fct_acidentes
dim_localidade


🧩 Macro DBT
Classificação de gravidade:
case  when vitima_fatal >= 5 then 'ALTA'  when vitima_fatal >= 1 then 'MEDIA'  else 'BAIXA'end

🧪 Testes de Qualidade
✔ Not Null
✔ Integridade
✔ Regras de negócio

```

---

## 📊 Dashboards (Superset)
📈 Visualizações Criadas

## 1. 📊 Acidentes por Município


Tipo: Bar Chart
Insight: cidades com maior incidência


## 2. 📉 Evolução Temporal


Tipo: Line Chart
Insight: tendência ao longo do tempo


## 3. 🧭 Gravidade dos Acidentes


Tipo: Scatter Plot
Insight: relação entre severidade




# 🚀 Como Executar


1. Subir ambiente
```bash
docker-compose up -d
```

2. Rodar DBT
```bash
dbt run
dbt test
dbt docs generate
dbt docs serve
```

3. Superset
Acesse:
```bash
http://localhost:8092
```
Login:admin
Pass: admin

## 🔗 Conexão Superset
```bash
postgresql://admin:admin123@ postgres_lab02:5433/acidentes_db
```
---
## 🎯 Resultados
```text
✔ Pipeline completo de dados
✔ Camada GOLD estruturada
✔ Dashboard interativo
✔ Governança com testes
✔ Projeto pronto para produção
```

## 📌 Insights Obtidos

```text
Municípios com maior número de acidentes
Evolução temporal de ocorrências
Relação entre gravidade e volume
```



💼 Autor

Edvaldo da Cruz Jr.
Projeto desenvolvido para Laboratório ( Lab02_NUSP) do curso Engenharia de Dados + big Data - Poli USP

```text
Engenharia de Dados 
Modelagem Analítica
Visualização de Dados
DataOps
```



