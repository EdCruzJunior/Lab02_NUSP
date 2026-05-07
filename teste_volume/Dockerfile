# base Docker image that we will build on
FROM python:3.14.3-slim 

# set up our image by installing prerequisites; pandas n this case
RUN pip install pandas pyarrow
RUN pip install uv

# set up the working directory inside the container
WORKDIR /app

# copy the script to the container. 1st name is source file, 2nd is destination
COPY pipeline.py pipeline.py
COPY app/requirements.txt .
COPY pyproject.toml uv.lock ./

RUN pip install --no-cache-dir -r requirements.txt
# instalar deps com uv
RUN uv sync

# copiar código
COPY app/ .

# define what to do first when the container runs
# in this example, we will just run the script
ENTRYPOINT [ "uv", "run", "python", "pipeline.py" ]

