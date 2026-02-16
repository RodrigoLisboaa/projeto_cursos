from db.connection import get_connection


def main():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
            result = cur.fetchone()
            print("Conexão OK. Resultado do SELECT 1:", result)


if __name__ == "__main__":
    main()
