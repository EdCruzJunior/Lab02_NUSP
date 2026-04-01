import os
import pandas as pd
from sqlalchemy import create_engine
import argparse

#=======================================
# baixar o arquivo csv de fonte externa
#=======================================
def download_csv():
    url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
    os.makedirs("data/raw", exist_ok=True)
    df = pd.read_csv(url)
    df.to_csv("data/raw/dados.csv", index=False)

# =============================
# CONFIG (IMPORTANTE no Docker)
# =============================
DB_HOST = "db"  # nome do serviço no docker-compose
DB_NAME = "pipeline_db"
DB_USER = "postgres"
DB_PASS = "SorteEngData5"
DB_PORT = "5432"

# =============================
# EXTRACT
# =============================
def extract():
    df = pd.read_csv("data/raw/dados.csv")
    return df

# =============================
# TRANSFORM
# =============================
def transform(df, regioes):
    df.columns = [col.lower().replace(" ", "_") for col in df.columns]

    if "regiao" in df.columns:
        df = df[df["regiao"].isin(regioes)]

    return df

# =============================
# SAVE PARQUET
# =============================
def save_parquet(df):
    os.makedirs("data/silver", exist_ok=True)
    df.to_parquet("data/silver/dados.parquet", index=False)

# =============================
# LOAD
# =============================
def load(df):
    conn = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(conn)

    df.to_sql("dados_tratados", engine, if_exists="replace", index=False)

# =============================
# MAIN
# =============================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("regioes", nargs="+")
    args = parser.parse_args()

    df = extract()
    df = transform(df, args.regioes)
    save_parquet(df)
    load(df)

    print("✅ Pipeline executado com sucesso!")

if __name__ == "__main__":
    main()