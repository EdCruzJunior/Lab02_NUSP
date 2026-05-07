import os
import time
import datetime
import pandas as pd
import requests
from sqlalchemy import create_engine
import great_expectations as gx
from great_expectations.core.batch import RuntimeBatchRequest


# =========================
# DOWNLOAD
# =========================
def download_csv():
    url = "https://dadosabertos.artesp.sp.gov.br/dataset/5e3af2a0-3b6a-4ee6-8556-b59b5d813ffc/resource/7aee242c-8be1-43ea-a2e7-d9525ec926d9/download/acidentes_2026.csv"

    os.makedirs("data/raw", exist_ok=True)

    print("⬇️ Baixando arquivo...")

    df = pd.read_csv(url)
    df.columns = df.columns.str.lower().str.strip()

    df.to_csv("data/raw/acidentes_2026.csv", index=False)

    print("✅ Download concluído")

    return df


# =========================
# ESPERAR BANCO
# =========================
def wait_for_db():
    for i in range(15):
        try:
            engine = create_engine(
                "postgresql://admin:admin123@postgres:5432/acidentes_db",
                pool_pre_ping=True
            )
            with engine.connect():
                print("✅ Banco conectado")
                return engine
        except:
            print(f"⏳ Tentativa {i+1}/15...")
            time.sleep(3)

    raise Exception("❌ Banco não disponível")


# =========================
# VALIDAÇÃO + MÉTRICAS
# =========================
def validate_data(df):

    print("🔍 Validando dados...")

    # Conversões
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    df["hora"] = pd.to_datetime(df["hora"], errors="coerce").dt.hour

    print("DATA nulos:", df["data"].isna().sum())
    print("HORA nulos:", df["hora"].isna().sum())
    print("KM inválido:", (~df["km"].between(0, 1000)).sum())
    print("LAT inválido:", (~df["latitude"].between(-90, 90)).sum())
    print("Sentidos:", df["sentido"].unique())

    # GX Context
    context = gx.get_context(context_root_dir="great_expectations")

    # Runtime Batch (FIX definitivo)
    batch_request = RuntimeBatchRequest(
        datasource_name="pandas_runtime",
        data_connector_name="runtime_data_connector",
        data_asset_name="acidentes_data",
        runtime_parameters={"batch_data": df},
        batch_identifiers={"default_identifier_name": "default_id"}
    )

    # criar suite se não existir
    try:
        context.add_expectation_suite("acidentes_suite")
    except:
        pass

    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite_name="acidentes_suite"
    )

    # =========================
    # EXPECTATIONS
    # =========================
    validator.expect_column_values_to_not_be_null("data")

    validator.expect_column_values_to_be_between(
        "km", min_value=0, max_value=1000
    )

    validator.expect_column_values_to_be_between(
        "latitude", min_value=-90, max_value=90
    )

    validator.expect_column_values_to_be_between(
        "hora", min_value=0, max_value=23
    )

    validator.expect_column_values_to_be_in_set(
        "sentido",
        ["NORTE", "SUL", "LESTE", "OESTE", "EXTERNO", "INTERNO"]
    )

    # =========================
    # EXECUTAR VALIDAÇÃO
    # =========================
    results = validator.validate()

    # gerar Data Docs
    context.build_data_docs()

    # =========================
    # 📊 MÉTRICAS (PASSO 1)
    # =========================
    os.makedirs("data/metrics", exist_ok=True)

    total_expectations = len(results.results)
    failed = sum([not r.success for r in results.results])
    success_rate = (
        (total_expectations - failed) / total_expectations * 100
        if total_expectations > 0 else 0
    )

    metrics = pd.DataFrame([{
        "timestamp": datetime.datetime.now(),
        "total_expectations": total_expectations,
        "failed": failed,
        "success_rate": round(success_rate, 2)
    }])

    metrics_path = "data/metrics/metrics.csv"

    if os.path.exists(metrics_path):
        metrics.to_csv(metrics_path, mode="a", header=False, index=False)
    else:
        metrics.to_csv(metrics_path, index=False)

    print("📊 Métricas registradas com sucesso")

    # =========================
    # LOG DE RESULTADO
    # =========================
    if not results.success:
        print("❌ Falha na qualidade dos dados")
        for r in results.results:
            if not r.success:
                print("➡️", r.expectation_config.expectation_type)
                print("   ", r.result)
    else:
        print("✅ Dados validados com sucesso")

    return df


# =========================
# MAIN
# =========================
def main():
    print("🚀 Pipeline iniciado")

    df = download_csv()
    df = validate_data(df)

    engine = wait_for_db()

    df.to_sql("acidentes_rodovias", engine, if_exists="replace", index=False)

    print("🎉 Pipeline finalizado")


if __name__ == "__main__":
    main()