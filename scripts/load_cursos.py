from pathlib import Path

from config import CSV_DIR
from core.cursos import normalizar_curso, validar_curso
from db.connection import get_connection
from scripts.loader import process_csv


def insert_curso(cur, curso: dict) -> bool:
    cur.execute(
        """
        INSERT INTO cursos (id, nome, ativo)
        VALUES (%s, %s, %s)
        ON CONFLICT (id) DO NOTHING
        RETURNING id
        """,
        (
            int(curso["id"]),
            curso["nome"],
            curso["ativo"] == "true",
        ),
    )
    return cur.fetchone() is not None


def main() -> None:
    caminho_csv = Path(CSV_DIR) / "cursos.csv"

    process_csv(
        csv_path=caminho_csv,
        normalize=normalizar_curso,
        validate=validar_curso,
        insert_row=insert_curso,
        get_connection=get_connection,
        entity_name="Curso",
        logger_name=__name__,
    )


if __name__ == "__main__":
    main()