import os
import psycopg

def get_connection():
    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname="mentoria_dev",
        user="postgres",
        password=os.getenv("PGPASSWORD", ""),
    )
