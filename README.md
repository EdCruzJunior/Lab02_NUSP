# 🚀 Pipeline de Engenharia de Dados com DBT + PostgreSQL + Apache Superset

## 📊 Visão Geral --

Este projeto demonstra a construção de um pipeline moderno de dados, transformando dados brutos em insights analíticos utilizando ferramentas amplamente utilizadas no mercado.

### 🎯 Objetivo
Transformar dados de acidentes (CSV) em uma camada analítica estruturada (GOLD) e disponibilizar insights através de dashboards interativos.

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

---

## 🐳 Ambiente (Docker Compose) --

📄 docker-compose.yml

```text
version: '3.8'services:  postgres:    image: postgres:15    container_name: postgres_lab02    environment:      POSTGRES_USER: admin      POSTGRES_PASSWORD: admin      POSTGRES_DB: acidentes_db    ports:      - "5432:5432"  superset:    build:      context: .      dockerfile: dockerfile.superset    container_name: superset    ports:      - "8089:8088"    environment:      SUPERSET_SECRET_KEY: lab_key    depends_on:      - postgres


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


Limpeza e padronização


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



📸 Prints (Adicionar no GitHub)
🔹 DBT Docs

🔹 Superset Dashboard


🚀 Como Executar
1. Subir ambiente
docker-compose up -d

2. Rodar DBT
dbt rundbt test

3. Superset
Acesse:
http://localhost:8089
Login:
admin / admin

🔗 Conexão Superset
postgresql://admin:admin@host.docker.internal:5432/acidentes_db

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



🚀 Próximos Passos


🔄 Incremental models (dbt)


⏱️ Orquestração com Airflow


🌎 Mapas geográficos


📊 KPIs avançados



💼 Autor
Projeto desenvolvido para demonstração de habilidades em:


Engenharia de Dados


Modelagem Analítica


Visualização de Dados


DataOps





🚀 ResultadoEsse README agora é:✔ Profissional (nível portfólio)  ✔ Explicativo (storytelling)  ✔ Reprodutível (docker-compose)  ✔ Visual (arquitetura + prints)  ✔ Valioso para recrutadores  ---# 👇 Se quiser dar mais um upgradePosso te ajudar a:- 📊 adicionar KPIs reais (taxa de fatalidade)- 🌎 incluir mapa interativo no Superset- 🧠 escrever insights prontos para entrevista- 💼 montar versão para LinkedInSó falar 👍