import argparse
import subprocess
import sys
import time
from typing import NoReturn


def sh(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def capture(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, text=True).strip()


def wait_postgres_healthy(container: str = "projeto_cursos_db", timeout_sec: int = 60) -> None:
    start = time.time()
    while True:
        try:
            status = capture(
                ["docker", "inspect", "--format", "{{.State.Health.Status}}", container]
            )
        except subprocess.CalledProcessError:
            status = ""

        if status == "healthy":
            return

        if time.time() - start >= timeout_sec:
            sh(["docker", "compose", "ps"])
            raise SystemExit(f"Postgres não ficou healthy em {timeout_sec}s")

        time.sleep(2)


def cmd_up(_: argparse.Namespace) -> None:
    sh(["docker", "compose", "up", "-d"])
    wait_postgres_healthy()


def cmd_down(_: argparse.Namespace) -> None:
    sh(["docker", "compose", "down"])


def cmd_ps(_: argparse.Namespace) -> None:
    sh(["docker", "compose", "ps"])


def cmd_logs(_: argparse.Namespace) -> None:
    sh(["docker", "compose", "logs", "-f", "db"])


def cmd_migrate(_: argparse.Namespace) -> None:
    wait_postgres_healthy()
    sh(["alembic", "upgrade", "head"])


def cmd_reset_db(_: argparse.Namespace) -> None:
    sh(["docker", "compose", "down", "-v"])
    sh(["docker", "compose", "up", "-d"])
    wait_postgres_healthy()
    sh(["alembic", "upgrade", "head"])


def cmd_run(_: argparse.Namespace) -> None:
    sh([sys.executable, "-m", "scripts.main"])


def cmd_install(_: argparse.Namespace) -> None:
    sh([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])


def cmd_lint(_: argparse.Namespace) -> None:
    sh(["ruff", "check", "."])


def cmd_fmt(_: argparse.Namespace) -> None:
    sh(["ruff", "format", "."])


def cmd_test(_: argparse.Namespace) -> None:
    sh(["pytest", "-q"])


def cmd_check(_: argparse.Namespace) -> None:
    sh(["ruff", "check", "."])
    sh(["pytest", "-q"])


def die(msg: str) -> NoReturn:
    print(msg, file=sys.stderr)
    raise SystemExit(2)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Task runner multiplataforma para o projeto (Docker/Alembic/Pipeline/Checks)."
    )
    sub = parser.add_subparsers(dest="task")

    def add(name: str, fn):
        p = sub.add_parser(name)
        p.set_defaults(fn=fn)

    add("up", cmd_up)
    add("down", cmd_down)
    add("ps", cmd_ps)
    add("logs", cmd_logs)
    add("migrate", cmd_migrate)
    add("reset-db", cmd_reset_db)
    add("run", cmd_run)
    add("install", cmd_install)
    add("lint", cmd_lint)
    add("fmt", cmd_fmt)
    add("test", cmd_test)
    add("check", cmd_check)

    args = parser.parse_args()
    if not getattr(args, "fn", None):
        die(
            "Uso: python tasks.py <task>\n"
            "Tasks: up, down, ps, logs, migrate, reset-db, run, install, "
            "lint, fmt, test, check"
        )
    args.fn(args)


if __name__ == "__main__":
    main()
