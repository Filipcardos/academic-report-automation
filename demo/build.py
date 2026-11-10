"""Gera a demonstração pública exclusivamente com os dados sintéticos do projeto."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from extractor import _seed_data
from reporter_excel import generate_excel
from reporter_pdf import generate_pdf
from transformer import transform_data


def build():
    output = ROOT / "demo" / "public"
    output.mkdir(exist_ok=True)
    raw = _seed_data()
    summaries = []
    courses = sorted({a["curso"] for a in raw["alunos"]})
    for i, course in enumerate([None, *courses]):
        ids = {a["id_aluno"] for a in raw["alunos"] if not course or a["curso"] == course}
        data = transform_data({k: [row for row in rows if row["id_aluno"] in ids]
                               for k, rows in raw.items()})
        prefix = f"relatorio-{i}"
        generate_excel(data, str(output / (prefix + ".xlsx")))
        generate_pdf(data, str(output / (prefix + ".pdf")))
        summaries.append({"curso": course or "Todos os cursos", "arquivo": prefix,
                          **{k: data[k] for k in ("total_alunos", "media_geral", "por_disciplina")}})
    page = (ROOT / "demo" / "template.html").read_text(encoding="utf-8")
    (output / "index.html").write_text(page.replace("__DATA__", json.dumps(summaries, ensure_ascii=True)), encoding="utf-8")


if __name__ == "__main__":
    build()
