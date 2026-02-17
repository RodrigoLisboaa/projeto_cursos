from logging_config import setup_logging
from scripts.load_alunos import main as load_alunos
from scripts.load_cursos import main as load_cursos
from scripts.load_matriculas import main as load_matriculas


def main() -> None:
    setup_logging()
    load_alunos()
    load_cursos()
    load_matriculas()


if __name__ == "__main__":
    main()
