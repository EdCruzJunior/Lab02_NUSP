import os 
import re
import time
import tempfile
import requests
import pandas as pd
from sqlalchemy import create_engine

# ==============================
# 🔐 CONFIGURAÇÃO
# ==============================
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_USER = os.getenv("DB_USER", "dbt")
DB_PASS = os.getenv("DB_PASS", "dbt")
DB_NAME = os.getenv("DB_NAME", "dbt_db")

CSV_PATH = os.getenv("CSV_PATH", "/app/raw/seeds/acidentes_rodovias_2026.csv")
#CSV_PATH = os.getenv("CSV_PATH", "https://drive.google.com/file/d/1B-tw0W4UhqPQsCDaOXxyr4P9OVu91NhQ/view?usp=sharing")
TABLE_NAME = os.getenv("TABLE_NAME", "acidentes_rodovias")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"

# ==============================
# 🔗 GOOGLE DRIVE HELPERS
# ==============================

def get_google_drive_file_id(url):
    match = re.search(r'/d/([A-Za-z0-9_-]+)', url)
    if match:
        return match.group(1)

    match = re.search(r'[?&]id=([A-Za-z0-9_-]+)', url)
    if match:
        return match.group(1)

    return None


def download_google_drive_file(url, destination_path):
    file_id = get_google_drive_file_id(url)
    if not file_id:
        raise ValueError(f"URL do Google Drive inválida: {url}")

    base_url = "https://drive.google.com/file/d/1B-tw0W4UhqPQsCDaOXxyr4P9OVu91NhQ/view?usp=sharing"
    session = requests.Session()

    response = session.get(base_url, params={"id": file_id}, stream=True)
    token = None
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            token = value
            break

    if token:
        response = session.get(base_url, params={"id": file_id, "confirm": token}, stream=True)

    with open(destination_path, "wb") as f:
        for chunk in response.iter_content(32768):
            if chunk:
                f.write(chunk)


# ==============================
# ⏳ AGUARDAR BANCO
# ==============================
def wait_for_db():
    while True:
        try:
            engine = create_engine(DATABASE_URL)
            with engine.connect() as conn:
                conn.exec_driver_sql("SELECT 1")
            print("✅ Banco disponível!")
            break
        except:
            print("⏳ Aguardando banco...")
            time.sleep(3)

# ==============================
# 📥 EXTRACT
# ==============================
def extract():
    print(f"📥 Lendo CSV: {CSV_PATH}")

    csv_path = CSV_PATH
    if CSV_PATH.startswith("https://") or CSV_PATH.startswith("http://"):
        print("📥 Download do arquivo do Google Drive...")
        csv_path = os.path.join(tempfile.gettempdir(), "acidentes_rodovias_2026.csv")
        download_google_drive_file(CSV_PATH, csv_path)

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {csv_path}")

    df = pd.read_csv(csv_path, sep=",", encoding="utf-8")

    print(f"✅ {len(df)} registros carregados")
    return df

# ==============================
# 🔄 TRANSFORM
# ==============================
def transform(df):
    print("🔄 Transformando dados...")

    # Padronizar colunas
    df.columns = [col.lower().strip() for col in df.columns]

    # Converter datas
    if "data" in df.columns:
        df["data"] = pd.to_datetime(df["data"], errors="coerce")

    # Converter hora
    if "hora" in df.columns:
        df["hora"] = df["hora"].astype(str)

    # Converter numéricos
    numeric_cols = [
        "km", "latitude", "longitude",
        "vitima_ilesa", "vitima_leve", "vitima_moderada",
        "vitima_grave", "vitima_fatal", "vitimas_sem_info",
        "veiculos_envolvidos"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Remover duplicados
    df = df.drop_duplicates()

    # Tratar nulos
    df = df.fillna({
        "municipio": "NAO INFORMADO",
        "rodovia": "NAO INFORMADO"
    })

    # Padronizar texto (upper)
    text_cols = ["municipio", "rodovia", "causa_provavel"]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.upper()

    print("✅ Transformação concluída")
    return df

# ==============================
# 💾 LOAD
# ==============================
def load(df):
    print(f"💾 Gravando dados na tabela: {TABLE_NAME}")

    engine = create_engine(DATABASE_URL)

    with engine.begin() as conn:
        df.to_sql(
            TABLE_NAME,
            conn,
            if_exists="replace",  # trocar para append em produção
            index=False,
            method="multi",
            chunksize=1000
        )

    print("✅ Dados carregados com sucesso!")

# ==============================
# 🚀 PIPELINE
# ==============================
def main():
    print("🚀 Iniciando pipeline de acidentes rodoviários...")

    wait_for_db()
    df = extract()
    df = transform(df)
    load(df)

    print("🎉 Pipeline finalizado!")

if __name__ == "__main__":
    main()