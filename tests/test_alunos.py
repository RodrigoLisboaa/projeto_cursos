from core.alunos import normalizar_aluno, validar_aluno


def test_normalizar_aluno_strip_lower_and_collapse_spaces():
    entrada = {"id": "  1 ", "nome": "  João   Santos  ", "email": "  TEST@EMAIL.COM  ", "idade": " 20 "}
    saida = normalizar_aluno(entrada)

    assert saida["id"] == "1"
    assert saida["nome"] == "João Santos"
    assert saida["email"] == "test@email.com"
    assert saida["idade"] == "20"


def test_validar_aluno_email_obrigatorio():
    linha = normalizar_aluno({"id": "1", "nome": "Ana", "email": "", "idade": "20"})
    erros = validar_aluno(linha)
    assert "email vazio" in erros


def test_validar_aluno_id_obrigatorio_e_numerico():
    linha = normalizar_aluno({"id": "", "nome": "Ana", "email": "a@a.com", "idade": "20"})
    assert "id vazio" in validar_aluno(linha)

    linha = normalizar_aluno({"id": "abc", "nome": "Ana", "email": "a@a.com", "idade": "20"})
    assert "id não é número" in validar_aluno(linha)


def test_validar_aluno_idade_obrigatoria_numerica_e_minima():
    linha = normalizar_aluno({"id": "1", "nome": "Ana", "email": "a@a.com", "idade": ""})
    assert "idade vazia" in validar_aluno(linha)

    linha = normalizar_aluno({"id": "1", "nome": "Ana", "email": "a@a.com", "idade": "abc"})
    assert "idade não é número" in validar_aluno(linha)

    linha = normalizar_aluno({"id": "1", "nome": "Ana", "email": "a@a.com", "idade": "15"})
    assert "idade menor que 16" in validar_aluno(linha)


def test_validar_aluno_ok_retorna_lista_vazia():
    linha = normalizar_aluno({"id": "1", "nome": "Ana", "email": "a@a.com", "idade": "16"})
    assert validar_aluno(linha) == []