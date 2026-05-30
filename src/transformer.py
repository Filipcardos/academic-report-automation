"""
Transformer — limpa, agrupa e calcula indicadores acadêmicos.
"""

import logging
from collections import defaultdict

log = logging.getLogger(__name__)


def transform_data(raw: dict) -> dict:
    alunos = raw["alunos"]
    notas = raw["notas"]
    matriculas = raw["matriculas"]
    # ── notas por aluno ─────────────────────────────────────────────────────
    notas_por_aluno = defaultdict(list)
    for n in notas:
        notas_por_aluno[n["id_aluno"]].append(n)

    # ── média por aluno ─────────────────────────────────────────────────────
    alunos_enriquecidos = []
    for a in alunos:
        ns = notas_por_aluno[a["id_aluno"]]

        media = round(sum(n["nota_final"] for n in ns) / len(ns), 2) if ns else 0.0

        freq = round(sum(n["frequencia"] for n in ns) / len(ns), 2) if ns else 0.0

        aprovado = all(n["situacao"] == "Aprovado" for n in ns) if ns else False

        alunos_enriquecidos.append(
            {
                **a,
                "media": media,
                "frequencia_media": freq,
                "situacao": "Aprovado" if aprovado else "Reprovado",
                "qtd_disc": len(ns),
            }
        )

    # ── indicadores gerais ──────────────────────────────────────────────────
    total = len(alunos_enriquecidos)

    aprovados = sum(1 for a in alunos_enriquecidos if a["situacao"] == "Aprovado")

    media_geral = (
        round(
            sum(a["media"] for a in alunos_enriquecidos) / total,
            2,
        )
        if total
        else 0
    )

    # ── por curso ───────────────────────────────────────────────────────────
    cursos_map = defaultdict(list)
    for a in alunos_enriquecidos:
        cursos_map[a["curso"]].append(a)

    por_curso = []
    for curso, lista in sorted(cursos_map.items()):
        apr = sum(1 for a in lista if a["situacao"] == "Aprovado")

        med = round(
            sum(a["media"] for a in lista) / len(lista),
            2,
        )

        por_curso.append(
            {
                "curso": curso,
                "total": len(lista),
                "aprovados": apr,
                "reprovados": len(lista) - apr,
                "taxa_aprovacao": round(apr / len(lista) * 100, 1),
                "media": med,
            }
        )

    # ── por disciplina ──────────────────────────────────────────────────────
    disc_map = defaultdict(list)
    for n in notas:
        disc_map[n["disciplina"]].append(n)

    por_disciplina = []
    for disc, lista in sorted(disc_map.items()):
        apr = sum(1 for n in lista if n["situacao"] == "Aprovado")

        med = round(
            sum(n["nota_final"] for n in lista) / len(lista),
            2,
        )

        por_disciplina.append(
            {
                "disciplina": disc,
                "total": len(lista),
                "aprovados": apr,
                "reprovados": len(lista) - apr,
                "taxa_aprovacao": round(apr / len(lista) * 100, 1),
                "media": med,
            }
        )

    # ── matrículas por modalidade ───────────────────────────────────────────
    mod_map = defaultdict(int)
    for m in matriculas:
        mod_map[m["modalidade"]] += 1

    por_modalidade = [{"modalidade": k, "total": v} for k, v in sorted(mod_map.items())]

    return {
        "alunos": alunos_enriquecidos,
        "por_curso": por_curso,
        "por_disciplina": por_disciplina,
        "por_modalidade": por_modalidade,
        "total_alunos": total,
        "total_aprovados": aprovados,
        "total_reprovados": total - aprovados,
        "media_geral": media_geral,
        "taxa_aprovacao": (round(aprovados / total * 100, 1) if total else 0),
    }
