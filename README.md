# 📊 Academic Report Automation

> Pipeline de automação que extrai dados acadêmicos do **SQL Server**, transforma indicadores e gera relatórios profissionais em **Excel** e **PDF** — containerizado com **Docker** e com **CI/CD via GitHub Actions**.

![CI/CD](https://github.com/Filipcardos/academic-report-automation/actions/workflows/ci-cd.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![SQL Server](https://img.shields.io/badge/SQL%20Server-2022-CC2927?logo=microsoftsqlserver)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🎯 Objetivo

Automatizar a geração periódica de relatórios acadêmicos (alunos, notas, matrículas) eliminando trabalho manual, garantindo rastreabilidade e entregando insights visuais para a gestão institucional.

---

## 🏗️ Arquitetura

```
SQL Server 2022
      │
      ▼
 extractor.py  ──►  transformer.py  ──►  reporter_excel.py  ──►  .xlsx
                                    └──►  reporter_pdf.py   ──►  .pdf
```

| Camada | Responsabilidade |
|--------|-----------------|
| **Extractor** | Conecta ao SQL Server via `pyodbc`, executa queries parametrizadas |
| **Transformer** | Limpa dados, calcula médias, taxas de aprovação e agrupa por curso/disciplina |
| **Reporter Excel** | Gera `.xlsx` com 4 abas, gráficos e formatação profissional (`openpyxl`) |
| **Reporter PDF** | Gera `.pdf` formatado com tabelas e indicadores (`ReportLab`) |

---

## 🚀 Como rodar

### Pré-requisitos
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado

### 1. Clone o repositório
```bash
git clone https://github.com/SEU_USUARIO/academic-report-automation.git
cd academic-report-automation
```

### 2. Configure as variáveis de ambiente
```bash
cp .env.example .env
# Edite .env com sua senha do SQL Server se necessário
```

### 3. Suba os containers
```bash
docker compose up --build
```

Os relatórios serão gerados na pasta `reports/` com timestamp no nome.

### 4. Modo demonstração (sem SQL Server)
```bash
docker run --rm \
  -e USE_SEED=true \
  -v $(pwd)/reports:/app/reports \
  academic-report-automation
```

---

## 🧪 Testes

```bash
pip install openpyxl reportlab pytest pytest-cov
USE_SEED=true PYTHONPATH=src pytest tests/ -v --cov=src
```

---

## ⚙️ CI/CD — GitHub Actions

O pipeline roda automaticamente a cada `push` na branch `main`:

```
push → main
    │
    ├──  test    → pytest + cobertura de código
    ├──  lint    → flake8
    ├──  build   → Docker image → GitHub Container Registry (ghcr.io)
    └──  run     → Executa container e salva relatórios como artefato
```

---

## 📁 Estrutura do projeto

```
academic-report-automation/
├── src/
│   ├── main.py              # Orquestrador do pipeline
│   ├── extractor.py         # Conexão SQL Server + seed de dados
│   ├── transformer.py       # Cálculo de indicadores
│   ├── reporter_excel.py    # Gerador .xlsx
│   └── reporter_pdf.py      # Gerador .pdf
├── tests/
│   └── test_pipeline.py     # Testes unitários
├── data/
│   └── init.sql             # Schema + dados iniciais SQL Server
├── .github/
│   └── workflows/
│       └── ci-cd.yml        # Pipeline GitHub Actions
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🛠️ Stack

| Tecnologia | Uso |
|---|---|
| Python 3.11 | Linguagem principal |
| SQL Server 2022 | Banco de dados relacional |
| pyodbc | Conector SQL Server |
| openpyxl | Geração de Excel com gráficos |
| ReportLab | Geração de PDF |
| Docker + Compose | Containerização |
| GitHub Actions | CI/CD automatizado |
| pytest | Testes unitários |

---

## 👤 Autor

**Filipe Oliveira Cardoso**
[LinkedIn](https://linkedin.com/in/filipe-cardoso-919532205) • [GitHub](https://github.com/Filipcardos)
