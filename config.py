import os

from dotenv import load_dotenv

load_dotenv()

CSV_DIR = os.getenv("CSV_DIR", "data")

PGHOST = os.getenv("PGHOST", "localhost")
PGPORT = int(os.getenv("PGPORT", "5432"))
PGDATABASE = os.getenv("PGDATABASE", "mentoria_dev")
PGUSER = os.getenv("PGUSER", "postgres")
PGPASSWORD = os.getenv("PGPASSWORD", "")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}",
)

SQLALCHEMY_DATABASE_URL = os.getenv(
    "SQLALCHEMY_DATABASE_URL",
    DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1),
)

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
