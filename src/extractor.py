"""
Extractor — conecta ao SQL Server e extrai dados acadêmicos.
Em ambiente de teste/demo usa dados sintéticos (seed).
"""

import logging
import os
import random
from datetime import date, timedelta

log = logging.getLogger(__name__)

# Variáveis de ambiente
DB_SERVER = os.getenv("DB_SERVER", "")
DB_NAME = os.getenv("DB_NAME", "AcademicDB")
DB_USER = os.getenv("DB_USER", "sa")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
USE_SEED = os.getenv("USE_SEED", "true").lower() == "true"

# Queries
SQL_ALUNOS = """
    SELECT
        a.id_aluno,
        a.nome,
        a.email,
        a.curso,
        a.periodo
    FROM dbo.Alunos a
    WHERE a.ativo = 1
"""

SQL_NOTAS = """
    SELECT
        n.id_aluno,
        n.disciplina,
        n.nota_final,
        n.frequencia,
        n.situacao  -- 'Aprovado' | 'Reprovado' | 'Cursando'
    FROM dbo.Notas n
    INNER JOIN dbo.Alunos a ON a.id_aluno = n.id_aluno
    WHERE a.ativo = 1
"""

SQL_MATRICULAS = """
    SELECT
        m.id_aluno,
        m.data_matricula,
        m.modalidade,  -- 'Presencial' | 'EAD'
        m.status  -- 'Ativa' | 'Trancada' | 'Concluida'
    FROM dbo.Matriculas m
"""


def _connect():
    """Retorna conexão pyodbc com SQL Server."""
    import pyodbc

    conn_str = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_NAME};"
        f"UID={DB_USER};"
        f"PWD={DB_PASSWORD};"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str, timeout=10)


def _seed_data():
    """Gera dados sintéticos para demo e testes."""
    random.seed(42)

    cursos = ["Medicina", "Enfermagem", "Fisioterapia", "Farmácia"]
    disciplinas = [
        "Anatomia",
        "Bioquímica",
        "Fisiologia",
        "Farmacologia",
        "Microbiologia",
    ]
    modalidades = ["Presencial", "EAD"]
    status_mat = ["Ativa", "Trancada", "Concluída"]

    alunos = [
        {
            "id_aluno": i,
            "nome": f"Aluno {i:03d}",
            "email": f"aluno{i:03d}@faculdade.edu.br",
            "curso": random.choice(cursos),
            "periodo": random.randint(1, 8),
        }
        for i in range(1, 81)
    ]

    notas = []
    for a in alunos:
        for disc in random.sample(disciplinas, k=random.randint(3, 5)):
            nota = round(random.uniform(3.0, 10.0), 1)
            freq = round(random.uniform(50.0, 100.0), 1)

            notas.append(
                {
                    "id_aluno": a["id_aluno"],
                    "disciplina": disc,
                    "nota_final": nota,
                    "frequencia": freq,
                    "situacao": (
                        "Aprovado" if nota >= 6.0 and freq >= 75.0 else "Reprovado"
                    ),
                }
            )

    base_date = date.today() - timedelta(days=365)

    matriculas = [
        {
            "id_aluno": a["id_aluno"],
            "data_matricula": (
                base_date + timedelta(days=random.randint(0, 300))
            ).isoformat(),
            "modalidade": random.choice(modalidades),
            "status": random.choices(status_mat, weights=[75, 10, 15])[0],
        }
        for a in alunos
    ]

    return {
        "alunos": alunos,
        "notas": notas,
        "matriculas": matriculas,
    }


def extract_data() -> dict:
    """
    Ponto de entrada principal.
    Usa banco real se DB_SERVER estiver configurado,
    caso contrário usa seed.
    """
    if USE_SEED or not DB_SERVER:
        log.info(" [SEED] Usando dados sintéticos.")
        return _seed_data()

    log.info(f"Conectando em {DB_SERVER}/{DB_NAME}...")
    conn = _connect()
    cursor = conn.cursor()

    def query(sql):
        cursor.execute(sql)
        cols = [c[0] for c in cursor.description]
        return [dict(zip(cols, row)) for row in cursor.fetchall()]

    result = {
        "alunos": query(SQL_ALUNOS),
        "notas": query(SQL_NOTAS),
        "matriculas": query(SQL_MATRICULAS),
    }

    conn.close()
    return result
