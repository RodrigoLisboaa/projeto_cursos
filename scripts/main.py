from logging_config import setup_logging
from scripts.load_alunos import main as load_alunos
from scripts.load_cursos import main as load_cursos


def main() -> None:
    setup_logging()
    load_alunos()
    load_cursos()


if __name__ == "__main__":
    main()
