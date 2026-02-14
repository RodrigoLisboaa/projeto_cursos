import csv
from pathlib import Path
import logging
logger = logging.getLogger(__name__)


from config import CSV_DIR
from core.alunos import normalizar_aluno, validar_aluno
from db.connection import get_connection


def main() -> None:
    caminho_csv = Path(CSV_DIR) / "alunos.csv"
    if not caminho_csv.exists():
        raise FileNotFoundError(f"CSV não encontrado: {caminho_csv}")
    
    validos: list[dict] = []
    invalidos: list[tuple[dict, list[str]]] = []

    with caminho_csv.open(mode="r", encoding="utf-8", newline="") as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            linha = normalizar_aluno(linha)
            erros = validar_aluno(linha)

            if erros:
                invalidos.append((linha, erros))
            else:
                validos.append(linha)

    inserted = 0
    with get_connection() as conn:
        with conn.cursor() as cur:
            for aluno in validos:
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
                if cur.fetchone() is not None:
                    inserted += 1

    for linha, erros in invalidos:
        logger.warning(
            "Aluno ID %s (%s) inválido: %s",
            linha.get("id"),
            linha.get("nome"),
            ", ".join(erros),
        )

    logger.info("Inseridos no banco: %s", inserted)
    logger.info("Inválidos no CSV: %s", len(invalidos))

if __name__ == "__main__":
    main()            
