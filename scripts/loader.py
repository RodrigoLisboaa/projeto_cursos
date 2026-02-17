import csv
import logging
from pathlib import Path
from typing import Any, Callable

NormalizeFn = Callable[[dict[str, Any]], dict[str, Any]]
ValidateFn = Callable[[dict[str, Any]], list[str]]
InsertFn = Callable[[Any, dict[str, Any]], bool]  # cursor, row -> inserted?


def process_csv(
    csv_path: Path,
    normalize: NormalizeFn,
    validate: ValidateFn,
    insert_row: InsertFn,
    get_connection: Callable[[], Any],
    entity_name: str,
    max_invalid_logs: int = 10,
    logger_name: str | None = None,
) -> None:
    """Pipeline genérico: lê CSV, valida, insere e loga resumo."""
    logger = logging.getLogger(logger_name or __name__)

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV não encontrado: {csv_path}")

    validos: list[dict[str, Any]] = []
    invalidos: list[tuple[dict[str, Any], list[str]]] = []

    with csv_path.open(mode="r", encoding="utf-8", newline="") as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            linha = normalize(linha)
            erros = validate(linha)
            if erros:
                invalidos.append((linha, erros))
            else:
                validos.append(linha)

    inserted = 0
    failed_inserts = 0

    with get_connection() as conn:
        with conn.cursor() as cur:
            for row in validos:
                if insert_row(cur, row):
                    inserted += 1
                else:
                    failed_inserts += 1

    # Log Inválidos (limitado)
    for i, (linha, erros) in enumerate(invalidos):
        if i >= max_invalid_logs:
            break
        logger.warning(
            "%s inválido: %s",
            _format_entity_line(entity_name, linha),
            ", ".join(erros),
        )

    if len(invalidos) > max_invalid_logs:
        logger.warning(
            "%s: %s inválidos adicionais não exibidos (limite=%s)",
            entity_name,
            len(invalidos) - max_invalid_logs,
            max_invalid_logs,
        )

    logger.info("%s - Inseridos no banco: %s", entity_name, inserted)
    logger.info("%s - Inválidos no CSV: %s", entity_name, len(invalidos))

    if failed_inserts:
        logger.info(
            "%s - Falhas na inserção (ex: FK/unique): %s",
            entity_name,
            failed_inserts,
        )


def _format_entity_line(entity_name: str, linha: dict[str, Any]) -> str:
    """
    Formata uma linha para log: 'Aluno ID 3 (João)' / 'Curso ID 2 (SQL)'.
    """
    id_ = linha.get("id")
    nome = linha.get("nome")
    if id_ is not None and nome is not None:
        return f"{entity_name} ID {id_} ({nome})"
    if id_ is not None:
        return f"{entity_name} ID {id_}"
    return f"{entity_name}"
