"""
Reporter PDF — gera relatório .pdf formatado com ReportLab.
"""

import logging
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

log = logging.getLogger(__name__)

# ── Paleta ──────────────────────────────────────────────────────────────
BLUE_DARK = colors.HexColor("#1F3864")
BLUE_MID = colors.HexColor("#2E75B6")
BLUE_LIGHT = colors.HexColor("#D6E4F0")
GREEN = colors.HexColor("#375623")
RED = colors.HexColor("#C00000")
GRAY_BG = colors.HexColor("#F2F2F2")
WHITE = colors.white


def _styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "title",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=18,
            textColor=BLUE_DARK,
            spaceAfter=4,
        ),
        "subtitle": ParagraphStyle(
            "subtitle",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10,
            textColor=colors.HexColor("#666666"),
            spaceAfter=12,
        ),
        "section": ParagraphStyle(
            "section",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            textColor=BLUE_MID,
            spaceBefore=16,
            spaceAfter=6,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10,
            spaceAfter=4,
        ),
    }


def _kpi_table(data):
    kpis = [
        ["Total de Alunos", str(data["total_alunos"])],
        ["Aprovados", str(data["total_aprovados"])],
        ["Reprovados", str(data["total_reprovados"])],
        ["Taxa de Aprovação", f"{data['taxa_aprovacao']}%"],
        ["Média Geral", f"{data['media_geral']:.2f}"],
    ]
    table = Table(kpis, colWidths=[7 * cm, 5 * cm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), BLUE_LIGHT),
                ("BACKGROUND", (1, 0), (1, -1), WHITE),
                ("TEXTCOLOR", (0, 0), (0, -1), BLUE_DARK),
                ("TEXTCOLOR", (1, 0), (1, -1), BLUE_DARK),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 11),
                ("ALIGN", (1, 0), (1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ROWBACKGROUND", (0, 0), (-1, -1), [BLUE_LIGHT, WHITE]),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#BFBFBF"),
                ),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    return table


def _build_table(rows):
    table = Table(rows, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), BLUE_MID),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        (
            "GRID",
            (0, 0),
            (-1, -1),
            0.5,
            colors.HexColor("#BFBFBF"),
        ),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]

    for i in range(1, len(rows)):
        bg = GRAY_BG if i % 2 == 0 else WHITE
        style.append(("BACKGROUND", (0, i), (-1, i), bg))

    table.setStyle(TableStyle(style))
    return table


def generate_pdf(data: dict, path: str):
    doc = SimpleDocTemplate(
        path,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title="Relatório Acadêmico",
    )

    styles = _styles()
    elements = []

    # Cabeçalho
    elements.append(Paragraph("Relatório Acadêmico", styles["title"]))
    elements.append(
        Paragraph(
            (
                "Gerado automaticamente em "
                f"{datetime.now().strftime('%d/%m/%Y às %H:%M')} "
                "via Academic Report Automation"
            ),
            styles["subtitle"],
        )
    )

    elements.append(HRFlowable(width="100%", thickness=2, color=BLUE_DARK))
    elements.append(Spacer(1, 0.4 * cm))

    # KPIs
    elements.append(Paragraph("Indicadores Gerais", styles["section"]))
    elements.append(_kpi_table(data))
    elements.append(Spacer(1, 0.5 * cm))

    # Curso
    elements.append(Paragraph("Desempenho por Curso", styles["section"]))
    curso_rows = [["Curso", "Total", "Aprovados", "Reprovados"]]
    for r in data["por_curso"]:
        curso_rows.append(
            [r["curso"], r["total"], r["aprovados"], r["reprovados"]]
        )
    elements.append(_build_table(curso_rows))
    elements.append(Spacer(1, 0.5 * cm))

    # Disciplina
    elements.append(
        Paragraph("Desempenho por Disciplina", styles["section"])
    )
    disc_rows = [["Disciplina", "Total", "Aprovados", "Reprovados"]]
    for r in data["por_disciplina"]:
        disc_rows.append(
            [r["disciplina"], r["total"], r["aprovados"], r["reprovados"]]
        )
    elements.append(_build_table(disc_rows))
    elements.append(Spacer(1, 0.5 * cm))

    # Rodapé
    elements.append(HRFlowable(width="100%", thickness=1, color=BLUE_MID))
    elements.append(Spacer(1, 0.2 * cm))
    elements.append(
        Paragraph(
            (
                "Academic Report Automation | Python + SQL Server + "
                "Docker + GitHub Actions"
            ),
            styles["subtitle"],
        )
    )

    doc.build(elements)
    log.info("PDF salvo: %s", path)
