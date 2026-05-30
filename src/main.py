"""
Main — orquestra o pipeline de dados acadêmicos.
"""

import logging

from extractor import extract_data
from reporter_excel import generate_excel
from reporter_pdf import generate_pdf
from transformer import transform_data

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def run_pipeline():
    log.info("Iniciando pipeline de dados acadêmicos...")

    raw = extract_data()

    log.info("Transformando dados...")
    processed = transform_data(raw)

    log.info("Gerando relatórios...")

    excel_path = "output/relatorio_academico.xlsx"
    pdf_path = "output/relatorio_academico.pdf"

    generate_excel(processed, excel_path)
    generate_pdf(processed, pdf_path)

    log.info(
        "Relatórios gerados com sucesso em: "
        f"{excel_path} e {pdf_path}"
    )


if __name__ == "__main__":
    run_pipeline()