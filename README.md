# 🚀 Projeto de Engenharia de Dados com dbt + PostgreSQL + Superset

## 📌 Visão Geral

Este projeto implementa um pipeline completo de dados utilizando:

* **dbt (Data Build Tool)** → transformação de dados
* **PostgreSQL** → armazenamento
* **Apache Superset** → visualização e dashboards
* **Docker Compose** → orquestração dos serviços

---

## 🧠 Arquitetura

```
CSV → dbt seed → staging → marts → PostgreSQL → Superset
```

---

## 📁 Estrutura do Projeto

```
.
├── docker-compose.yml
├── dbt_project.yml
├── profiles.yml
├── seeds/
│   └── acidentes_rodovias_2026.csv
├── models/
│   ├── staging/
│   │   └── stg_acidentes.sql
│   ├── marts/
│   │   ├── dim_localidade.sql
│   │   └── fct_acidentes.sql
├── snapshots/
│   └── snapshot_acidentes.sql
├── dags/ (opcional - Airflow)
```

---

## 🐳 Docker Compose

### Subir ambiente:

```bash
docker compose up -d
```

### Parar ambiente:

```bash
docker compose down --remove-orphans
```

---

## ⚙️ Configuração do dbt

### profiles.yml

```yaml
acidentes_projeto:
  target: dev
  outputs:
    dev:
      type: postgres
      host: postgres
      user: dbt
      password: dbt
      port: 5432
      dbname: dbt_db
      schema: public
      threads: 2
```

---

## 🌱 Executar pipeline dbt

### Rodar debug

```bash
docker compose run dbt debug
```

### Carregar dados (CSV)

```bash
docker compose run dbt seed
```

### Executar modelos

```bash
docker compose run dbt run
```

### Executar snapshots

```bash
docker compose run dbt snapshot
```

### Executar tudo

```bash
docker compose run dbt build
```

---

## 📊 Acessar banco PostgreSQL

```bash
docker exec -it lab02_nusp-postgres-1 psql -U dbt -d dbt_db
```

Exemplo:

```sql
SELECT * FROM staging.stg_acidentes LIMIT 10;
SELECT * FROM marts.fct_acidentes LIMIT 10;
```

---

## 📈 Configurar Apache Superset

### Acessar:

```
http://localhost:8088
```

### Criar conexão com banco:

```
postgresql://dbt:dbt@postgres:5432/dbt_db
```

---

## 📊 Criar Dataset

* Schema: `marts`
* Tabela: `fct_acidentes`

---

## 📈 Exemplo de Query Analítica

```sql
SELECT
    municipio,
    COUNT(*) AS total_acidentes
FROM marts.fct_acidentes
GROUP BY municipio
ORDER BY total_acidentes DESC;
```

---

## 🔄 Pipeline de Dados

1. `dbt seed` → carrega CSV
2. `dbt run` → transforma dados
3. `dbt snapshot` → histórico
4. Superset → visualização

---

## ⚠️ Problemas comuns

### ❌ dbt não conecta ao banco

* Verificar `host: postgres`
* Verificar containers ativos

### ❌ Container dbt não sobe

```bash
docker compose logs dbt
```

### ❌ Superset não conecta

* Usar hostname `postgres`
* Verificar porta 5432

---

## 🧪 Testes

```bash
docker compose run dbt test
```

---

## 💡 Boas práticas

* Usar `staging` para limpeza de dados
* Usar `marts` para análise
* Não usar `SELECT *` em produção
* Versionar tudo com Git

---

## 🚀 Evoluções possíveis

* Orquestração com Airflow
* Dashboards avançados
* Modelos incrementais
* Monitoramento e alertas

---

## 👨‍💻 Autor

Projeto desenvolvido para estudo de Engenharia de Dados.

---
