import os
import time
import pandas as pd
import requests
from sqlalchemy import create_engine
import great_expectations as ge


# =========================
# DOWNLOAD
# =========================
def download_csv():
    url = "https://dadosabertos.artesp.sp.gov.br/dataset/5e3af2a0-3b6a-4ee6-8556-b59b5d813ffc/resource/7aee242c-8be1-43ea-a2e7-d9525ec926d9/download/acidentes_2026.csv"

    output_path = "data/raw/acidentes_2026.csv"
    os.makedirs("data/raw", exist_ok=True)

    print("⬇️ Baixando arquivo...")

    response = requests.get(url, timeout=60)
    response.raise_for_status()

    with open(output_path, "wb") as f:
        f.write(response.content)

    df = pd.read_csv(output_path, encoding="utf-8")

    # normaliza colunas
    df.columns = df.columns.str.lower().str.strip()

    print("✅ Download e normalização concluídos")

    return df


# =========================
# ESPERAR BANCO
# =========================
def wait_for_db():
    for _ in range(10):
        try:
            engine = create_engine("postgresql://admin:admin123@postgres:5432/acidentes_db")
            conn = engine.connect()
            conn.close()
            print("✅ Conectado ao banco")
            return engine
        except Exception:
            print("⏳ Aguardando banco...")
            time.sleep(3)
    raise Exception("❌ Banco não disponível")


# =========================
# VALIDAÇÃO + TRATAMENTO
# =========================
def validate_data(df):

    print("🔍 Validando dados...")

    # validar estrutura
    required_cols = ["data", "hora", "km", "latitude", "sentido"]
    missing = [c for c in required_cols if c not in df.columns]

    if missing:
        raise Exception(f"❌ Colunas ausentes: {missing}")

    # conversões
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    df["hora"] = pd.to_datetime(df["hora"], errors="coerce").dt.hour

    # debug rápido
    print("DATA nulos:", df["data"].isna().sum())
    print("HORA nulos:", df["hora"].isna().sum())
    print("KM inválido:", (~df["km"].between(0, 1000)).sum())
    print("LAT inválido:", (~df["latitude"].between(-90, 90)).sum())
    print("Sentidos encontrados:", df["sentido"].unique())

    # Great Expectations
    gdf = ge.from_pandas(df)

    gdf.expect_column_values_to_not_be_null("data")
    gdf.expect_column_values_to_be_between("km", 0, 1000)
    gdf.expect_column_values_to_be_between("latitude", -90, 90)
    gdf.expect_column_values_to_be_between("hora", 0, 23)
    gdf.expect_column_values_to_be_in_set(
        "sentido",
        ["NORTE", "SUL", "OESTE", "LESTE", "EXTERNO", "INTERNO"]
    )

    results = gdf.validate()

    # 🔍 Mostrar falhas detalhadas
    for r in results["results"]:
        if not r["success"]:
            print("❌ Falha:", r["expectation_config"]["expectation_type"])
            print("➡️ Detalhes:", r["result"])

    # =========================
    # SEPARAÇÃO DE DADOS
    # =========================
    valid_df = df[
        df["data"].notna() &
        df["hora"].between(0, 23) &
        df["km"].between(0, 1000) &
        df["latitude"].between(-90, 90)
    ]

    invalid_df = df[~df.index.isin(valid_df.index)]

    # salvar dados inválidos
    if not invalid_df.empty:
        os.makedirs("data/error", exist_ok=True)
        invalid_df.to_csv("data/error/invalid_data.csv", index=False)
        print(f"⚠️ {len(invalid_df)} registros inválidos salvos em data/error/")

    print(f"✅ Registros válidos: {len(valid_df)}")

    return valid_df


# =========================
# MAIN
# =========================
def main():
    print("🚀 Iniciando pipeline...")

    df = download_csv()
    df = validate_data(df)

    engine = wait_for_db()

    df.to_sql("acidentes_rodovias", engine, if_exists="replace", index=False)

    print("🎉 Pipeline executado com sucesso!")


# =========================
# EXECUÇÃO
# =========================
if __name__ == "__main__":
    main()