import os 
import time
import pandas as pd
from sqlalchemy import create_engine, text

# ==============================
# 🔐 CONFIGURAÇÃO
# ==============================
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASS = os.getenv("DB_PASS", "admin123")
DB_NAME = os.getenv("DB_NAME", "acidentes_db")

CSV_PATH = os.getenv("CSV_PATH", "/app/raw/acidentes_rodovias.csv")
TABLE_NAME = os.getenv("TABLE_NAME", "acidentes_rodovias")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"

# ==============================
# ⏳ AGUARDAR BANCO
# ==============================
def wait_for_db():
    while True:
        try:
            engine = create_engine(DATABASE_URL)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
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

    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"Arquivo não encontrado: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH, sep=",", encoding="utf-8")

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