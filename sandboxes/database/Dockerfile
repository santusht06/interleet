FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python database and query testing libraries
RUN pip install --no-cache-dir \
    mongomock==4.3.0 \
    pymongo==4.10.1 \
    "redis==4.6.0" \
    "fakeredis==2.20.0" \
    sqlglot==26.0.0

WORKDIR /app

# Copy runner
COPY runner.py /app/runner.py
RUN chmod +x /app/runner.py

WORKDIR /workspace

CMD ["python3", "/app/runner.py"]
