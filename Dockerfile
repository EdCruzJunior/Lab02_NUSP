<<<<<<< HEAD
# base Docker image that we will build on
FROM python:3.14.3-slim 


# set up our image by installing prerequisites; pandas n this case
RUN pip install pandas pyarrow

# set up the working directory inside the container
WORKDIR /app

# copy the script to the container. 1st name is source file, 2nd is destination
COPY pipeline.py pipeline.py
COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
#RUN pip install great_expectations

# define what to do first when the container runs
# in this example, we will just run the script
ENTRYPOINT [ "python", "pipeline.py" ]

=======
# Imagem base leve
FROM python:3.11-slim 
FROM apache/superset:latest

USER root
RUN pip install psycopg2-binary
USER superset



# Variáveis de ambiente (boas práticas)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho
WORKDIR /app

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
COPY /app .

# Criar pastas necessárias
RUN mkdir -p /app/raw /root/.dbt

# Comando padrão
CMD ["python", "pipeline.py"]
>>>>>>> 77de25478af48ad189d80f8de42e0fe0a5dfd690
