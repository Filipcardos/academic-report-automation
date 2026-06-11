"""
Testes unitários — transformer e geração de relatórios.
"""

import os

import pytest

from extractor import _seed_data
from transformer import transform_data


@pytest.fixture(scope="module")
def processed():
    raw = _seed_data()
    return transform_data(raw)


# ── Extractor ───────────────────────────────────────────────────────────
def test_seed_has_alunos():
    raw = _seed_data()
    assert len(raw["alunos"]) == 80


def test_seed_has_notas():
    raw = _seed_data()
    assert len(raw["notas"]) > 0


def test_seed_has_matriculas():
    raw = _seed_data()
    assert len(raw["matriculas"]) == 80


# ── Transformer ─────────────────────────────────────────────────────────
def test_total_alunos(processed):
    assert processed["total_alunos"] == 80


def test_aprovados_plus_reprovados(processed):
    assert processed["total_aprovados"] + processed[
        "total_reprovados"
    ] == processed["total_alunos"]


def test_taxa_aprovacao_range(processed):
    assert 0 <= processed["taxa_aprovacao"] <= 100


def test_media_geral_range(processed):
    assert 0 <= processed["media_geral"] <= 10


def test_por_curso_nao_vazio(processed):
    assert len(processed["por_curso"]) > 0


def test_por_disciplina_nao_vazio(processed):
    assert len(processed["por_disciplina"]) > 0


def test_por_curso_soma_total(processed):
    soma = sum(c["total"] for c in processed["por_curso"])
    assert soma == processed["total_alunos"]


def test_aluno_tem_media(processed):
    for a in processed["alunos"]:
        assert "media" in a
        assert 0 <= a["media"] <= 10


# ── Reporter Excel ──────────────────────────────────────────────────────
def test_generate_excel(processed, tmp_path):
    from reporter_excel import generate_excel

    path = str(tmp_path / "test.xlsx")
    generate_excel(processed, path)

    assert os.path.exists(path)
    assert os.path.getsize(path) > 5000


# ── Reporter PDF ────────────────────────────────────────────────────────
def test_generate_pdf(processed, tmp_path):
    from reporter_pdf import generate_pdf

    path = str(tmp_path / "test.pdf")

    generate_pdf(processed, path)

    assert os.path.exists(path)
    assert os.path.getsize(path) > 2000
