from pathlib import Path

from db.connection import get_connection

def run_sql_file(conn, filepath: Path) -> None:
    sql = filepath.read_text(encoding="utf-8")

    with conn.cursor() as cur:
        cur.execute(sql)

def main() -> None:
    sql_dir = Path(__file__).resolve().parent / "sql"
    reset_file = sql_dir / "00_reset_schema.sql"
    create_file = sql_dir / "01_create_tables.sql"

    if not reset_file.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {reset_file}")
    if not create_file.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {create_file}")
    
    with get_connection() as conn:
        run_sql_file(conn, reset_file)
        run_sql_file(conn, create_file)

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT to_regclass('public.alunos')  AS alunos,
                       to_regclass('public.cursos') AS cursos,
                       to_regclass('public.matriculas') AS matriculas;
                """
            )
            row = cur.fetchone()
        print("Setup OK. Tabelas:", row)

if __name__ == "__main__":
    main()