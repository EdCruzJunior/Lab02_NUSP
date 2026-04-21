# Imagem base leve
FROM python:3.11-slim 




# Variáveis de ambiente (boas práticas)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho
WORKDIR /

# Instalar dependências do sistema (opcional, mas comum)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    gcc \
    python3-dev \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar dependências primeiro (cache eficiente)
COPY requirements.txt .

# instalar dbt corretamente via pip
RUN pip install --no-cache-dir dbt-postgres

# Instalar libs Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY / .

# Criar pastas necessárias
RUN mkdir -p /app/raw /root/.dbt

# Comando padrão
CMD ["python", "pipeline.py"]