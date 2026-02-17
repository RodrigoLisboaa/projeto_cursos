from core.matriculas import normalizar_matricula, validar_matricula


def test_normalizar_matricula_strip():
    entrada = {"id": " 1 ", "aluno_id": " 2 ", "curso_id": " 3 ", "data_matricula": " 2026-02-16 "}
    saida = normalizar_matricula(entrada)
    assert saida["id"] == "1"
    assert saida["aluno_id"] == "2"
    assert saida["curso_id"] == "3"
    assert saida["data_matricula"] == "2026-02-16"


def test_validar_matricula_data_invalida():
    linha = normalizar_matricula(
        {"id": "1", "aluno_id": "1", "curso_id": "1", "data_matricula": "2026-13-01"}
    )
    assert "data_matricula inválida (use YYYY-MM-DD)" in validar_matricula(linha)
