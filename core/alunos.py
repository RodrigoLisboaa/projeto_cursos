def normalizar_aluno(linha:dict) -> dict:
    return {
        "id": (linha.get("id") or "").strip(),
        "nome": " ".join(((linha.get("nome") or "").strip()).split()),
        "email": ((linha.get("email") or "").strip()).lower(),
        "idade": (linha.get("idade") or "").strip(),
    }

def validar_aluno(linha: dict) -> list[str]:
    erros = []

    # email obrigatório
    if not linha["email"]:
        erros.append("email vazio")

    # nome obrigatório
    if not linha["nome"]:
        erros.append("nome vazio")

    # idade obrigatória, numérica e >=16
    if not linha["idade"]:
        erros.append("idade vazia")
    else:
        try:
            idade = int(linha["idade"])
            if idade < 16:
                erros.append("idade menor que 16")
        except ValueError:
            erros.append("idade não é número")

    #id obrigatório
    if not linha["id"]:
        erros.append("id vazio")
    else:
        try:
            int(linha["id"])
        except ValueError:
            erros.append("id não é número")

    return erros