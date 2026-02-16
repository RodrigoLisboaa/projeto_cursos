from core.cursos import normalizar_curso, validar_curso


def test_normalizar_curso_strip_collapse_spaces_and_lower():
    entrada = {"id": "  2 ", "nome": "  SQL   para  Dados  ", "ativo": " TRUE "}
    saida = normalizar_curso(entrada)

    assert saida["id"] == "2"
    assert saida["nome"] == "SQL para Dados"
    assert saida["ativo"] == "true"


def test_validar_curso_id_obrigatorio_e_numerico():
    linha = normalizar_curso({"id": "", "nome": "Python", "ativo": "true"})
    assert "id vazio" in validar_curso(linha)

    linha = normalizar_curso({"id": "x", "nome": "Python", "ativo": "true"})
    assert "id não é número" in validar_curso(linha)


def test_validar_curso_nome_obrigatorio():
    linha = normalizar_curso({"id": "1", "nome": "", "ativo": "true"})
    assert "nome vazio" in validar_curso(linha)


def test_validar_curso_ativo_deve_ser_true_ou_false():
    linha = normalizar_curso({"id": "1", "nome": "Python", "ativo": ""})
    assert "ativo inválido (use true/false)" in validar_curso(linha)

    linha = normalizar_curso({"id": "1", "nome": "Python", "ativo": "yes"})
    assert "ativo inválido (use true/false)" in validar_curso(linha)


def test_validar_curso_ok_retorna_lista_vazia():
    linha = normalizar_curso({"id": "1", "nome": "Python", "ativo": "false"})
    assert validar_curso(linha) == []
