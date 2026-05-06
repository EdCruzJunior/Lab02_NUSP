import os
import time
import pandas as pd
import requests
from sqlalchemy import create_engine
import great_expectations as gx


# =========================
# DOWNLOAD
# =========================
def download_csv():
    url = "https://dadosabertos.artesp.sp.gov.br/dataset/5e3af2a0-3b6a-4ee6-8556-b59b5d813ffc/resource/7aee242c-8be1-43ea-a2e7-d9525ec926d9/download/acidentes_2026.csv"

    os.makedirs("data/raw", exist_ok=True)

    response = requests.get(url, timeout=60)
    response.raise_for_status()

    df = pd.read_csv(url)
    df.columns = df.columns.str.lower().str.strip()

    df.to_csv("data/raw/acidentes_2026.csv", index=False)

    return df


# =========================
# DB
# =========================
def wait_for_db():
    for _ in range(15):
        try:
            engine = create_engine(
                "postgresql://admin:admin123@postgres:5432/acidentes_db",
                pool_pre_ping=True
            )
            with engine.connect():
                return engine
        except:
            time.sleep(3)
    raise Exception("DB não disponível")


# =========================
# VALIDATION GX
# =========================
def validate_data(df):

    context = gx.get_context(context_root_dir="great_expectations")

    # cria datasource fluente (idempotente)
    datasource = context.sources.add_pandas("pandas_fs")

    asset = datasource.add_dataframe_asset("acidentes_raw")

    batch_request = asset.build_batch_request(dataframe=df)

    suite = context.add_or_update_expectation_suite("acidentes_suite")

    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite=suite
    )

    # Expectations
    validator.expect_column_values_to_not_be_null("data")
    validator.expect_column_values_to_be_between("km", 0, 1000)
    validator.expect_column_values_to_be_between("latitude", -90, 90)

    df["hora"] = pd.to_datetime(df["hora"], errors="coerce").dt.hour

    validator.expect_column_values_to_be_between("hora", 0, 23)

    validator.expect_column_values_to_be_in_set(
        "sentido",
        ["NORTE", "SUL", "LESTE", "OESTE", "EXTERNO", "INTERNO"]
    )

    validator.save_expectation_suite()

    results = validator.validate()

    if not results.success:
        print("❌ Falha na qualidade")

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

    print("✅ Pipeline finalizado")


if __name__ == "__main__":
    main()