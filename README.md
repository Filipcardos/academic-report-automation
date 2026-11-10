# Academic Report Automation

**[Abrir demonstração na Vercel ↗](https://academic-report-automation.vercel.app)**

Escolha um curso para consultar a média das notas e a taxa de aprovação por disciplina. Os mesmos indicadores estão disponíveis em uma planilha Excel para análise e em um PDF para compartilhar.

A demonstração usa dados fictícios de 80 alunos de Medicina, Enfermagem, Fisioterapia e Farmácia. Experimente selecionar **Medicina** e baixar a planilha: as abas **Dashboard**, **Por Curso**, **Por Disciplina** e **Alunos** passam a mostrar apenas esse recorte.

## Como funciona

O módulo de extração em Python lê alunos, notas e matrículas do SQL Server ou gera uma base fictícia. O módulo de transformação calcula os indicadores. O Excel é gerado com openpyxl e o PDF com ReportLab.

Na Vercel, [o script de publicação](demo/build.py) prepara a página e os arquivos a partir da base fictícia. Cada curso tem seu próprio par de relatórios, além da opção **Todos os cursos**.

## Executar a demonstração localmente

Na raiz do repositório, com Python 3.11:

```bash
python -m pip install openpyxl reportlab
python demo/build.py
python -m http.server 8000 --directory demo/public
```

Abra [localhost:8000](http://localhost:8000). A página, as planilhas e os PDFs ficam em `demo/public/`.

## Integração com SQL Server

As consultas estão em [src/extractor.py](src/extractor.py) e o esquema de exemplo em [data/init.sql](data/init.sql). Para usar o extrator com um banco próprio, configure `USE_SEED=false`, `DB_SERVER`, `DB_NAME`, `DB_USER` e `DB_PASSWORD` no ambiente do processo. Essa modalidade requer o pacote `pyodbc` e o ODBC Driver 18 for SQL Server.

## Testes

Na raiz do projeto:

```bash
python -m pip install openpyxl reportlab pytest
python -m pytest -o pythonpath=src tests/ -q
```

**Filipe Oliveira Cardoso** · [GitHub](https://github.com/Filipcardos) · [LinkedIn](https://www.linkedin.com/in/filipe-cardoso-919532205/)
