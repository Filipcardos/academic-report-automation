# ─────────────────────────────────────────────────────────────
# Academic Report Automation
# ─────────────────────────────────────────────────────────────

FROM python:3.11-slim

WORKDIR /app

# Dependências necessárias para Excel e PDF
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependências Python
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY src/ ./src/

# Diretório de saída
RUN mkdir -p /app/reports

# Variáveis de ambiente
ENV USE_SEED=true
ENV OUTPUT_DIR=/app/reports
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

CMD ["python", "src/main.py"]
