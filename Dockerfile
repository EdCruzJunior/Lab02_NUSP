# Imagem base leve
FROM python:3.11-slim 

# Variáveis de ambiente (boas práticas)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema (opcional, mas comum)
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar dependências primeiro (cache eficiente)
COPY app/requirements.txt .

# Instalar libs Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY app/ .

# Criar pasta de dados (se necessário)
RUN mkdir -p /data/raw

# Comando padrão
CMD ["python", "pipeline.py"]