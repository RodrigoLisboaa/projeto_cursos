def normalizar_curso(linha: dict) -> dict:
    return {
        "id": (linha.get("id") or "").strip(),
        "nome": " ".join(((linha.get("nome") or "").strip()).split()),
        "ativo": ((linha.get("ativo") or "").strip()).lower(),
    }


def validar_curso(linha: dict) -> list[str]:
    erros = []

    if not linha["id"]:
        erros.append("id vazio")
    else:
        try:
            int(linha["id"])
        except ValueError:
            erros.append("id não é número")

    if not linha["nome"]:
        erros.append("nome vazio")

    if linha["ativo"] not in {"true", "false"}:
        erros.append("ativo inválido (use true/false)")

    return erros
