from pathlib import Path

from config import CSV_DIR
from core.alunos import normalizar_aluno, validar_aluno
from db.connection import get_connection
from scripts.loader import process_csv


def insert_aluno(cur, aluno: dict) -> bool:
    cur.execute(
        """
        INSERT INTO alunos (id, nome, email, idade)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
        RETURNING id
        """,
        (
            int(aluno["id"]),
            aluno["nome"],
            aluno["email"],
            int(aluno["idade"]),
        ),
    )
    return cur.fetchone() is not None


def main() -> None:
    caminho_csv = Path(CSV_DIR) / "alunos.csv"

    process_csv(
        csv_path=caminho_csv,
        normalize=normalizar_aluno,
        validate=validar_aluno,
        insert_row=insert_aluno,
        get_connection=get_connection,
        entity_name="Aluno",
        logger_name=__name__,
    )


if __name__ == "__main__":
    main()
