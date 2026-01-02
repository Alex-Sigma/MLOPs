# Airflow image that supports Apple Silicon (multi-arch)
FROM apache/airflow:2.9.3-python3.12

USER root

# Minimal build tools (safe; useful if any pip wheels need compiling)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

USER airflow

# Install uv (your project uses uv.lock)
RUN pip install --no-cache-dir uv

# Copy dependency manifests and install deps into the image
WORKDIR /opt/airflow
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

# (optional) Make sure src is importable
ENV PYTHONPATH=/opt/airflow/src
