CREATE TABLE alunos (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    idade INTEGER NOT NULL CHECK (idade >= 16)
);

CREATE TABLE cursos (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    ativo BOOLEAN NOT NULL
);

CREATE TABLE matriculas (
    id INTEGER PRIMARY KEY,
    aluno_id INTEGER NOT NULL,
    curso_id INTEGER NOT NULL,
    data_matricula DATE NOT NULL,

    CONSTRAINT fk_matriculas_alunos
        FOREIGN KEY (aluno_id) REFERENCES alunos(id),

    CONSTRAINT fk_matriculas_cursos
        FOREIGN KEY (curso_id) REFERENCES cursos(id),

    CONSTRAINT uq_aluno_curso
        UNIQUE (aluno_id, curso_id)
);
