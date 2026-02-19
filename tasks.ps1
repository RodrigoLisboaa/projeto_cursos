param([Parameter(Mandatory=$true)][string]$task)

switch ($task) {
  "up"       { docker compose up -d }
  "down"     { docker compose down }
  "ps"       { docker compose ps }
  "logs"     { docker compose logs -f db }
  "reset-db" { docker compose down -v; docker compose up -d; python -m scripts.setup_db }
  "setup-db" { python -m scripts.setup_db }
  "run"      { python -m scripts.main }
  "install"  { pip install -r requirements.txt }
  "test"     { pytest -q }
  "lint"     { ruff check . }
  "fmt"      { ruff format . }
  "check"    { ruff check .; pytest -q }
  default    { Write-Host "Tasks: up, down, ps, logs, reset-db, setup-db, run, install, test, lint, fmt, check" }
}
