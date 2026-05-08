# README.md — Pipeline de Engenharia de Dados com PostgreSQL, Great Expectations e Apache Superset

---

# 🚀 Visão Geral do Projeto

Este projeto implementa um pipeline completo de engenharia de dados utilizando:

* PostgreSQL como camada de armazenamento
* Great Expectations para qualidade e observabilidade de dados
* Apache Superset para visualização analítica e dashboards
* Docker para containerização
* Python + Pandas para ingestão e transformação

---

# 🎯 Objetivo do Projeto

O objetivo é construir um pipeline de dados moderno capaz de:

* ingerir dados públicos de acidentes rodoviários
* validar qualidade dos dados
* armazenar informações estruturadas
* gerar métricas analíticas
* disponibilizar dashboards para análise de negócio

---

# 🛣️ Sobre os Dados

Os dados utilizados são provenientes da ARTESP (Agência Reguladora de Transporte do Estado de São Paulo).

Dataset utilizado:

```text
acidentes_2026.csv
```

Os dados representam acidentes ocorridos em rodovias e incluem informações como:

| Campo     | Descrição                |
| --------- | ------------------------ |
| data      | data do acidente         |
| hora      | hora do acidente         |
| km        | quilômetro da rodovia    |
| latitude  | coordenada geográfica    |
| longitude | coordenada geográfica    |
| sentido   | direção da pista         |
| rodovia   | identificação da rodovia |

---

# 🧱 Arquitetura do Projeto

```text
Fonte CSV
   ↓
Pipeline Python
   ↓
Camada RAW
   ↓
Great Expectations (Qualidade)
   ↓
PostgreSQL
   ↓
Camada GOLD (Views/KPIs)
   ↓
Apache Superset (Dashboard BI)
```

---

# 📁 Estrutura do Projeto

```text
project/
│
├── app/
│   ├── requirements.txt
│
├── data/
│   ├── raw/
│   ├── metrics/
│
├── great_expectations/
│
├── docker-compose.yml
├── Dockerfile
├── Dockerfile.superset
├── pipeline.py
└── README.md
```

---

# 🐳 Docker e PostgreSQL

## Subindo os containers

```bash
docker-compose up --build
```

---

# 🗄️ PostgreSQL

Banco utilizado:

```text
acidentes_db
```

Tabela principal:

```text
acidentes_rodovias
```

String de conexão:

```text
postgresql://admin:admin123@postgres:5432/acidentes_db
```

---

# Great Expectations (Qualidade de Dados)
O que é Great Expectations

Great Expectations é uma ferramenta de Data Quality utilizada para:

validação de dados
observabilidade
monitoramento
documentação de qualidade
geração de Data Docs

O framework permite criar regras chamadas de Expectations, responsáveis por validar consistência, formato e integridade dos dados.

📂 Estrutura do Great Expectations
great_expectations/
│
├── expectations/
├── checkpoints/
├── uncommitted/
├── validations/
└── great_expectations.yml
📂 Pasta expectations/

Responsável por armazenar as suítes de validação (Expectation Suites).

Arquivos
.ge_store_backend_id

Arquivo interno utilizado pelo Great Expectations para controle do backend de armazenamento das expectations.

acidentes_suite.json

Arquivo contendo todas as regras de validação criadas para o dataset.

Exemplo de expectativas armazenadas:

campos não nulos
valores válidos
ranges permitidos
conjuntos válidos
📂 Pasta checkpoints/

Responsável por armazenar checkpoints de execução.

Os checkpoints representam execuções organizadas das validações.

Arquivos
.ge_store_backend_id

Arquivo interno utilizado pelo GX para controle do armazenamento.

acidentes_checkpoint.yml

Arquivo YAML contendo:

expectation suite utilizada
datasource
batch request
ações executadas
geração de Data Docs

Exemplo:

name: acidentes_checkpoint
config_version: 1.0
📂 Pasta uncommitted/

Contém artefatos temporários e arquivos gerados automaticamente durante as execuções.

📂 data_docs/local_site/

Responsável pelos Data Docs.

Os Data Docs são páginas HTML geradas automaticamente contendo:

resultados das validações
métricas
histórico
status de sucesso/falha

Arquivo principal:

index.html

Abertura:

great_expectations/uncommitted/data_docs/local_site/index.html
📂 validations/

Responsável por armazenar os resultados históricos das validações executadas.

Cada execução do pipeline gera um novo registro de validação.

Arquivos
.ge_store_backend_id

Arquivo interno utilizado pelo Great Expectations para controle dos resultados armazenados.

---

# ✅ As 5 Expectativas Implementadas

---

## 1. Valores não nulos

```python
expect_column_values_to_not_be_null("data")
```

### Objetivo

Garantir que todos os registros possuam data válida.

---

## 2. KM válido

```python
expect_column_values_to_be_between(
    "km",
    min_value=0,
    max_value=1000
)
```

### Objetivo

Garantir que o quilômetro da rodovia esteja em faixa válida.

---

## 3. Latitude válida

```python
expect_column_values_to_be_between(
    "latitude",
    min_value=-90,
    max_value=90
)
```

### Objetivo

Validar coordenadas geográficas.

---

## 4. Hora válida

```python
expect_column_values_to_be_between(
    "hora",
    min_value=0,
    max_value=23
)
```

### Objetivo

Garantir formato correto de hora.

---

## 5. Valores permitidos para Sentido

```python
expect_column_values_to_be_in_set(
    "sentido",
    ["NORTE", "SUL", "LESTE", "OESTE", "EXTERNO", "INTERNO"]
)
```

### Objetivo

Garantir padronização do sentido da via.

---

# 📊 Data Docs (Observabilidade)

Após a execução do pipeline, o Great Expectations gera automaticamente documentação HTML contendo:

* resultados das validações
* histórico
* métricas de qualidade

Arquivo gerado:

```text
great_expectations/uncommitted/data_docs/local_site/index.html
```
<img width="1894" height="871" alt="image" src="https://github.com/user-attachments/assets/bb85c981-72b6-4e23-bac4-667b67c11730" />


---

# 📈 Métricas de Qualidade

O pipeline também registra métricas em:

```text
data/metrics/metrics.csv
```

Métricas calculadas:

| Métrica            | Descrição              |
| ------------------ | ---------------------- |
| success_rate       | percentual de sucesso  |
| failed             | expectativas com falha |
| total_expectations | total de validações    |
| timestamp          | horário da execução    |

---

# 🏆 Camada GOLD

Foi criada uma view analítica contendo KPIs agregados:

```sql
CREATE OR REPLACE VIEW vw_acidentes_gold AS
SELECT
    DATE(data) AS data,
    sentido,
    COUNT(*) AS total_acidentes,
    ROUND(AVG(km)::numeric, 2) AS km_medio,
    COUNT(*) FILTER (WHERE latitude IS NULL) AS erros_lat,
    COUNT(*) FILTER (WHERE km < 0 OR km > 1000) AS erros_km
FROM acidentes_rodovias
GROUP BY DATE(data), sentido
ORDER BY data;
```

---

# 📊 Apache Superset

## Objetivo

O Superset foi utilizado para construção de dashboards analíticos e visualização de dados.

---

# 🐳 Inicializando o Container do Superset

## Docker Compose

```yaml
superset:
  image: apache/superset:latest-dev
  container_name: superset
  ports:
    - "8088:8088"
```

---

# ▶️ Subir o Superset

```bash
docker-compose up -d
```

---

# 🔧 Inicialização do Superset

Entrar no container:

```bash
docker exec -it superset bash
```

---

# Executar comandos de setup

## Atualizar banco interno

```bash
superset db upgrade
```

---

## Criar usuário administrador

```bash
superset fab create-admin \
  --username admin \
  --firstname Admin \
  --lastname User \
  --email admin@admin.com \
  --password admin
```

---

## Inicializar Superset

```bash
superset init
```

---

# 🌐 Acessar Interface

```text
http://localhost:8088
```

Usuário:

```text
admin
```

Senha:

```text
admin
```

---

# 🔌 Conectar PostgreSQL no Superset

Connection String:

```text
postgresql://admin:admin123@postgres:5432/acidentes_db
```

---

# 📊 Dashboard Criado

Dashboard:

```text
Dashboard Acidentes Rodoviários
```

---

# 📈 Os 5 Gráficos Desenvolvidos

---

# 1️⃣ KPI — Total de Acidentes

### Tipo

Big Number

### Objetivo

Mostrar volume total de acidentes registrados.

---

# 2️⃣ KPI — KM Médio

### Tipo

Big Number

### Objetivo

Mostrar média do quilômetro dos acidentes.

---

# 3️⃣ Linha — Evolução Temporal

### Tipo

Time Series Line Chart

### Objetivo

Analisar tendência temporal de acidentes.

---

# 4️⃣ Barra — Acidentes por Sentido

### Tipo

Bar Chart

### Objetivo

Identificar distribuição por direção da rodovia.

---

# 5️⃣ Scatter Plot — KM Médio por Data

### Tipo

Scatter Plot

### Objetivo

Analisar comportamento espacial e distribuição dos acidentes.

---
<img width="1903" height="910" alt="image" src="https://github.com/user-attachments/assets/42902a48-5b2e-4f2d-a69b-8d49d949fa33" />

---
# 📌 Resultados Obtidos

O projeto permitiu:

* ingestão automatizada
* validação de qualidade
* observabilidade dos dados
* armazenamento estruturado
* construção de dashboards analíticos
* criação de KPIs para negócio

---

# 🚀 Melhorias Futuras

Possíveis evoluções:

* integração com Apache Airflow
* alertas automáticos
* ingestão incremental
* camada Silver em Parquet
* monitoramento em tempo real
* dashboard geográfico

---

# 🧠 Conclusão

Este projeto implementa uma arquitetura moderna de engenharia de dados utilizando:

* qualidade de dados
* governança
* visualização analítica
* observabilidade
* containerização

A solução permite escalabilidade e evolução para ambientes produtivos de dados.
