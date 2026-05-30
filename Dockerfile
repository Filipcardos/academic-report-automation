# ── Build stage ────────────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app

# Dependências do sistema para pyodbc (ODBC Driver)
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc g++ unixodbc-dev curl gnupg \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list \
        > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt


# ── Runtime stage ───────────────────────────────────────────────────────────────
FROM python:3.11-slim AS runtime

WORKDIR /app

# Copiar ODBC e libs do builder
COPY --from=builder /root/.local /root/.local
COPY --from=builder /usr/lib/x86_64-linux-gnu /usr/lib/x86_64-linux-gnu
COPY --from=builder /opt/microsoft /opt/microsoft
COPY --from=builder /etc/odbcinst.ini /etc/odbcinst.ini

# Código fonte
COPY src/ ./src/

# Diretório de saída
RUN mkdir -p /app/reports

# Variáveis de ambiente (sobrescreva via docker run -e ou .env)
ENV USE_SEED=true \
    OUTPUT_DIR=/app/reports \
    PYTHONUNBUFFERED=1 \
    PATH="/root/.local/bin:$PATH"

CMD ["python", "src/main.py"]
