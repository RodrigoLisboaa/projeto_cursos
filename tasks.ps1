param([Parameter(Mandatory=$true)][string]$task)

function Wait-PostgresHealthy {
  param(
    [string]$Container = "projeto_cursos_db",
    [int]$TimeoutSec = 60
  )

  $start = Get-Date
  while ($true) {
    $health = docker inspect --format "{{.State.Health.Status}}" $Container 2>$null

    if ($health -eq "healthy") { return }

    if (((Get-Date) - $start).TotalSeconds -ge $TimeoutSec) {
      docker compose ps | Out-Host
      throw "Postgres não ficou healthy em ${TimeoutSec}s"
    }

    Start-Sleep -Seconds 2
  }
}

switch ($task) {
  "up"        { docker compose up -d; Wait-PostgresHealthy }
  "down"      { docker compose down }
  "ps"        { docker compose ps }
  "logs"      { docker compose logs -f db }

  # Alembic (padrão do projeto)
  "migrate"   { Wait-PostgresHealthy; alembic upgrade head }
  "reset-db"  { docker compose down -v; docker compose up -d; Wait-PostgresHealthy; alembic upgrade head }

  # Execução do pipeline
  "run"       { python -m scripts.main }

  # Ambiente / qualidade
  "install"   { pip install -r requirements.txt }
  "test"      { pytest -q }
  "lint"      { ruff check . }
  "fmt"       { ruff format . }
  "check"     { ruff check .; pytest -q }

  default {
    Write-Host "Tasks: up, down, ps, logs, migrate, reset-db, run, install, test, lint, fmt, check"
  }
}
