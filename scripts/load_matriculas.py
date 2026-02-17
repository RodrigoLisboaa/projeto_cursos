from __future__ import annotations

import logging
from pathlib import Path

import psycopg
from psycopg.errors import ForeignKeyViolation, UniqueViolation

from config import CSV_DIR
from core.matriculas import normalizar_matricula, validar_matricula
from db.connection import get_connection
from scripts.loader import process_csv

logger = logging.getLogger(__name__)


def insert_matricula(cur, row: dict) -> bool:
    try:
        cur.execute(
            """
            INSERT INTO matriculas (id, aluno_id, curso_id, data_matricula)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
            RETURNING id
            """,
            (
                int(row["id"]),
                int(row["aluno_id"]),
                int(row["curso_id"]),
                row["data_matricula"],  # ISO string ok pra DATE
            ),
        )
        return cur.fetchone() is not None

    except ForeignKeyViolation:
        # FK violada: aluno_id ou curso_id não existe
        # precisamos limpar o erro da transação
        cur.connection.rollback()
        logger.warning(
            "Matrícula inválida (FK): id=%s, aluno_id=%s, curso_id=%s",
            row.get("id"),
            row.get("aluno_id"),
            row.get("curso_id"),
        )
        return False

    except UniqueViolation:
        # duplicata (aluno_id, curso_id) ou outro unique
        cur.connection.rollback()
        logger.warning(
            "Matrícula duplicada: (aluno_id, curso_id): aluno_id=%s curso_id=%s",
            row.get("aluno_id"),
            row.get("curso_id"),
        )
        return False

    except psycopg.Error:
        cur.connection.rollback()
        logger.exception("Erro ao inserir matrícula: %s", row)
        return False


def main() -> None:
    caminho_csv = Path(CSV_DIR) / "matriculas.csv"

    process_csv(
        csv_path=caminho_csv,
        normalize=normalizar_matricula,
        validate=validar_matricula,
        insert_row=insert_matricula,
        get_connection=get_connection,
        entity_name="Matrícula",
        logger_name=__name__,
    )


if __name__ == "__main__":
    main()
