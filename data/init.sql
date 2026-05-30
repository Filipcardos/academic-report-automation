-- ============================================================
-- AcademicDB — Schema e dados iniciais
-- ============================================================

IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'AcademicDB')
    CREATE DATABASE AcademicDB;
GO

USE AcademicDB;
GO

-- ── Tabelas ───────────────────────────────────────────────────────────────────

IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Alunos' AND xtype='U')
CREATE TABLE dbo.Alunos (
    id_aluno  INT           IDENTITY(1,1) PRIMARY KEY,
    nome      NVARCHAR(100) NOT NULL,
    email     NVARCHAR(150) NOT NULL UNIQUE,
    curso     NVARCHAR(80)  NOT NULL,
    periodo   TINYINT       NOT NULL,
    ativo     BIT           NOT NULL DEFAULT 1,
    criado_em DATETIME2     NOT NULL DEFAULT SYSDATETIME()
);

IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Notas' AND xtype='U')
CREATE TABLE dbo.Notas (
    id_nota    INT           IDENTITY(1,1) PRIMARY KEY,
    id_aluno   INT           NOT NULL REFERENCES dbo.Alunos(id_aluno),
    disciplina NVARCHAR(80)  NOT NULL,
    nota_final DECIMAL(4,1)  NOT NULL,
    frequencia DECIMAL(5,2)  NOT NULL,
    situacao   NVARCHAR(20)  NOT NULL,  -- Aprovado | Reprovado | Cursando
    criado_em  DATETIME2     NOT NULL DEFAULT SYSDATETIME()
);

IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Matriculas' AND xtype='U')
CREATE TABLE dbo.Matriculas (
    id_matricula  INT           IDENTITY(1,1) PRIMARY KEY,
    id_aluno      INT           NOT NULL REFERENCES dbo.Alunos(id_aluno),
    data_matricula DATE          NOT NULL,
    modalidade    NVARCHAR(20)  NOT NULL,  -- Presencial | EAD
    status        NVARCHAR(20)  NOT NULL   -- Ativa | Trancada | Concluída
);

-- ── Dados de exemplo ──────────────────────────────────────────────────────────

IF NOT EXISTS (SELECT TOP 1 1 FROM dbo.Alunos)
BEGIN
    INSERT INTO dbo.Alunos (nome, email, curso, periodo) VALUES
        ('Ana Souza',          'ana.souza@faculdade.edu.br',          'Medicina',      2),
        ('Bruno Lima',         'bruno.lima@faculdade.edu.br',         'Enfermagem',    3),
        ('Carla Mendes',       'carla.mendes@faculdade.edu.br',       'Fisioterapia',  1),
        ('Daniel Rocha',       'daniel.rocha@faculdade.edu.br',       'Farmácia',      4),
        ('Eduarda Ferreira',   'eduarda.ferreira@faculdade.edu.br',   'Medicina',      5),
        ('Felipe Cardoso',     'felipe.cardoso@faculdade.edu.br',     'Medicina',      2),
        ('Gabriela Costa',     'gabriela.costa@faculdade.edu.br',     'Enfermagem',    6),
        ('Hugo Alves',         'hugo.alves@faculdade.edu.br',         'Fisioterapia',  3),
        ('Isabela Nunes',      'isabela.nunes@faculdade.edu.br',      'Farmácia',      1),
        ('João Pereira',       'joao.pereira@faculdade.edu.br',       'Medicina',      7);

    INSERT INTO dbo.Notas (id_aluno, disciplina, nota_final, frequencia, situacao) VALUES
        (1, 'Anatomia',     8.5,  92.0, 'Aprovado'),
        (1, 'Bioquímica',   7.0,  88.0, 'Aprovado'),
        (2, 'Anatomia',     5.5,  70.0, 'Reprovado'),
        (2, 'Fisiologia',   9.0,  95.0, 'Aprovado'),
        (3, 'Farmacologia', 6.5,  80.0, 'Aprovado'),
        (4, 'Microbiologia',4.0,  60.0, 'Reprovado'),
        (5, 'Anatomia',     9.5,  98.0, 'Aprovado'),
        (6, 'Bioquímica',   7.5,  85.0, 'Aprovado'),
        (7, 'Fisiologia',   6.0,  76.0, 'Aprovado'),
        (8, 'Farmacologia', 3.5,  55.0, 'Reprovado'),
        (9, 'Microbiologia',8.0,  90.0, 'Aprovado'),
        (10,'Anatomia',     7.0,  82.0, 'Aprovado');

    INSERT INTO dbo.Matriculas (id_aluno, data_matricula, modalidade, status) VALUES
        (1,  '2024-02-01', 'Presencial', 'Ativa'),
        (2,  '2024-02-01', 'EAD',        'Ativa'),
        (3,  '2024-02-01', 'Presencial', 'Ativa'),
        (4,  '2023-08-01', 'EAD',        'Trancada'),
        (5,  '2023-02-01', 'Presencial', 'Ativa'),
        (6,  '2024-02-01', 'Presencial', 'Ativa'),
        (7,  '2022-08-01', 'EAD',        'Concluída'),
        (8,  '2024-02-01', 'Presencial', 'Ativa'),
        (9,  '2024-02-01', 'EAD',        'Ativa'),
        (10, '2021-02-01', 'Presencial', 'Ativa');
END
GO
