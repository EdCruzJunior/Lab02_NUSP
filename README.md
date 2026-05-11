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

```yaml
lab02_dbt:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost
      user: admin
      password: admin
      port: 5432
      dbname: acidentes_db
      schema: public
```
---

## 📂 7. Estrutura do Projeto

```
models/
├── staging/
│   ├── sources.yml
│   └── stg_acidentes.sql
├── marts/
│   ├── dim_localidade.sql
│   └── fct_acidentes.sql
macros/
tests/
```

---
## 🔗 8. Sources

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

### staging
```sql
select * from {{ source('raw','acidentes_raw') }}
```

### mart (fato)
```sql
select municipio, count(*) as total
from {{ ref('stg_acidentes') }}
group by municipio
```

---

## 🧪 10. Testes

```yaml
models:
  - name: fct_acidentes
    columns:
      - name: municipio
        tests:
          - not_null
```

---

## 📊 11. Documentação

```bash
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

---

## 🎯 Resultado Final

✔ Pipeline completo funcionando  
✔ Camada GOLD pronta  
✔ Dashboard interativo  

---

## 🧱 Stack Tecnológica


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

---

## Limpeza e padronização
Seleção de colunas relevantes


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

📊 Dashboards (Superset)
📈 Visualizações Criadas
1. 📊 Acidentes por Município


Tipo: Bar Chart
Insight: cidades com maior incidência


2. 📉 Evolução Temporal


Tipo: Line Chart
Insight: tendência ao longo do tempo


3. 🧭 Gravidade dos Acidentes


Tipo: Scatter Plot
Insight: relação entre severidade



🚀 Como Executar
1. Subir ambiente
docker-compose up -d

2. Rodar DBT
dbt rundbt test

3. Superset
Acesse:
http://localhost:8092
Login:
admin / admin

🔗 Conexão Superset
postgresql://admin:admin123@ postgres_lab02:5433/acidentes_db

🎯 Resultados
✔ Pipeline completo de dados
✔ Camada GOLD estruturada
✔ Dashboard interativo
✔ Governança com testes
✔ Projeto pronto para produção

📌 Insights Obtidos


Municípios com maior número de acidentes
Evolução temporal de ocorrências
Relação entre gravidade e volume



💼 Autor
Projeto desenvolvido para demonstração de habilidades em:


Engenharia de Dados
Modelagem Analítica
Visualização de Dados
DataOps


