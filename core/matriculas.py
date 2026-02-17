from __future__ import annotations

from datetime import date


def normalizar_matricula(linha: dict) -> dict:
    return {
        "id": (linha.get("id") or "").strip(),
        "aluno_id": (linha.get("aluno_id") or "").strip(),
        "curso_id": (linha.get("curso_id") or "").strip(),
        "data_matricula": (linha.get("data_matricula") or "").strip(),
    }


def validar_matricula(linha: dict) -> list[str]:
    erros: list[str] = []

    # id obrigatório e numérico
    if not linha["id"]:
        erros.append("id vazio")
    else:
        try:
            int(linha["id"])
        except ValueError:
            erros.append("id não é número")

    # aluno_id obrigatório e númérico
    if not linha["aluno_id"]:
        erros.append("aluno_id vazio")
    else:
        try:
            int(linha["aluno_id"])
        except ValueError:
            erros.append("aluno_id não é número")

    # curso_id obrigatório e númérico
    if not linha["curso_id"]:
        erros.append("curso_id vazio")
    else:
        try:
            int(linha["curso_id"])
        except ValueError:
            erros.append("curso_id não é número")

    # data obrigatória e válida
    if not linha["data_matricula"]:
        erros.append("data_matricula vazia")
    else:
        try:
            date.fromisoformat(linha["data_matricula"])
        except ValueError:
            erros.append("data_matricula inválida (use YYYY-MM-DD)")

    return erros
