#Dockerfiles
FROM apache/airflow:3.1.0-python3.12

USER root
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
USER airflow

WORKDIR /opt/airflow

# ✅ copy the file you actually install
COPY requirements.runtime.lock ./
RUN pip install --no-cache-dir -r requirements.runtime.lock

ENV PYTHONPATH=/opt/airflow/src