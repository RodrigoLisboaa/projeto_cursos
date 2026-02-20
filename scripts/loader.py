import csv
import json
import logging
import os
import unicodedata
from datetime import datetime
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

    # Export opcional de inválidos (antes dos logs, pra não "perder" nada)
    export_path = _maybe_export_invalids(entity_name, csv_path, invalidos, logger)

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

    if export_path is not None:
        logger.info("%s - Inválidos exportados em: %s", entity_name, export_path)


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


def _slug(text: str) -> str:
    """
    Normaliza para um identificador seguro (ASCII), removendo acentos.
    Ex: 'Matrícula' -> 'matricula'
    """
    text = text.strip().lower().replace(" ", "_")
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return text


def _maybe_export_invalids(
    entity_name: str,
    csv_path: Path,
    invalidos: list[tuple[dict[str, Any], list[str]]],
    logger: logging.Logger,
) -> Path | None:
    """
    Exporta inválidos se EXPORT_INVALIDS=1.
    Config via env:
      - EXPORT_INVALIDS: 0/1 (default 0)
      - INVALIDS_DIR: diretório de saída (default out/invalids)
      - INVALIDS_FORMAT: csv|json (default csv)
    """
    export_invalids = os.getenv("EXPORT_INVALIDS", "0").strip() == "1"
    if not export_invalids:
        return None

    if not invalidos:
        return None

    out_dir = Path(os.getenv("INVALIDS_DIR", "out/invalids"))
    fmt = os.getenv("INVALIDS_FORMAT", "csv").strip().lower()

    out_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_entity = _slug(entity_name)
    safe_input = _slug(csv_path.stem)

    if fmt not in {"csv", "json"}:
        logger.warning("INVALIDS_FORMAT inválido (%s). Usando csv.", fmt)
        fmt = "csv"

    out_path = out_dir / f"invalidos_{safe_entity}_{safe_input}_{timestamp}.{fmt}"

    if fmt == "json":
        payload = [
            {"row": row, "errors": errors, "entity": entity_name, "source": str(csv_path)}
            for row, errors in invalidos
        ]
        out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return out_path

    # CSV: coluna errors + união das chaves encontradas nos rows
    keys: set[str] = set()
    for row, _errors in invalidos:
        keys.update(row.keys())

    # Ordem estável: id/nome/email/idade/aluno_id/curso_id/data_matricula primeiro, resto depois
    preferred = [
        "id",
        "nome",
        "email",
        "idade",
        "aluno_id",
        "curso_id",
        "data_matricula",
    ]
    ordered_keys = [k for k in preferred if k in keys] + sorted(
        k for k in keys if k not in preferred
    )

    fieldnames = ["entity", "source", "errors", *ordered_keys]

    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row, errors in invalidos:
            record: dict[str, Any] = {
                "entity": entity_name,
                "source": str(csv_path),
                "errors": " | ".join(errors),
            }
            for k in ordered_keys:
                record[k] = row.get(k, "")
            writer.writerow(record)

    return out_path
