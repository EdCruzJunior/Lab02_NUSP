import os
import pandas as pd
import requests

def download_csv():
    url = "https://dadosabertos.artesp.sp.gov.br/dataset/5e3af2a0-3b6a-4ee6-8556-b59b5d813ffc/resource/7aee242c-8be1-43ea-a2e7-d9525ec926d9/download/acidentes_2026.csv"
    
    output_path = "data/raw/acidentes_2026.csv"
    os.makedirs("data/raw", exist_ok=True)

    try:
        print("⬇️ Baixando arquivo...")

        response = requests.get(url, timeout=60)
        response.raise_for_status()

        # Salva bruto (garante reprocessamento futuro)
        with open(output_path, "wb") as f:
            f.write(response.content)

        print("✅ Download concluído")

        # Lê com pandas tratando encoding
        df = pd.read_csv(output_path, encoding="utf-8", sep=",")

        # Normaliza colunas
        df.columns = df.columns.str.lower().str.strip()

        # Salva novamente padronizado
        df.to_csv(output_path, index=False)

        print("📁 Arquivo salvo e padronizado em:", output_path)

        return df

    except Exception as e:
        print(f"❌ Erro no download: {e}")
        raise


# Executar
if __name__ == "__main__":
    df = download_csv()
    print(df.head())