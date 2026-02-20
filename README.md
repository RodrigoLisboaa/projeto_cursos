# Python ETL Pipeline: CSV → PostgreSQL

Pipeline de ingestão focado em boas práticas: ambiente reprodutível com Docker, schema versionado com Alembic, qualidade garantida com ruff/pytest + CI. Inclui validação/normalização e export opcional de registros inválidos.

## Highlights (o que este projeto demonstra)

- **Reprodutibilidade:** Docker + Postgres com reset e migração em 1 comando (`.\tasks.ps1 reset-db`)
- **Schema versionado:** migrações com **Alembic** (`alembic upgrade head`)
- **Qualidade:** `ruff` (lint/format) + `pytest` + **CI** no GitHub Actions
- **Operação:** logging configurável + **export opcional de inválidos** (CSV/JSON)

---

## Status

- [x] Leitura de CSV (`csv.DictReader`)
- [x] Normalização e validação (`core/`)
- [x] Pipeline genérico de carga (`scripts/loader.py`)
- [x] Logging configurável (`LOG_LEVEL`)
- [x] Migrações com Alembic (schema versionado)
- [x] Carga no PostgreSQL (com `ON CONFLICT DO NOTHING`)
- [x] Testes com `pytest`
- [x] Padronização com `ruff` (lint/format)
- [x] CI com GitHub Actions (ruff + pytest)
- [x] Docker básico (PostgreSQL via `docker compose`)
- [x] Task runner (PowerShell) (`tasks.ps1`)
- [x] Export opcional de inválidos (CSV/JSON)

Próximos passos (planejados):
- [ ] Inserção em lote (bulk insert) para cenários com grandes volumes (ex.: `COPY`/batch)
- [ ] Task runner multiplataforma (ex.: `tasks.py`) para Mac/Linux
- [ ] Melhorias pequenas de usabilidade/documentação

---

## Estrutura do projeto

- `core/`  
  Regras de **normalização** e **validação** por entidade.
- `data/`  
  Arquivos `.csv` de entrada.
- `db/`  
  Conexão com o PostgreSQL.
- `scripts/`  
  Scripts de carga (ETL).
- `alembic/`  
  Migrações e versionamento de schema.
- `tests/`  
  Testes de normalização e validação.

---

## Requisitos

- Python 3.11+ (recomendado)
- Docker Desktop (recomendado) — para rodar o PostgreSQL
- Opcional: PostgreSQL local (fluxo alternativo / best effort)
- Dependências principais:
  - `psycopg[binary]`
  - `python-dotenv`

Dependências completas em `requirements.txt`.

---

## Configuração (.env)

1) Copie o arquivo de exemplo:

```bash
copy .env.example .env
```

2) Ajuste o `.env` se necessário (principalmente `PGPASSWORD`, `PGDATABASE` e `PGPORT`).

O projeto lê as variáveis via `config.py`. O `.env` não deve ser commitado (está no `.gitignore`).

## Como rodar (Docker - recomendado)

> **Importante:** execute os comandos a partir da **raiz** do projeto.

### 1) Suba o PostgreSQL (Docker)

```bash
.\tasks.ps1 up
.\tasks.ps1 ps
```

### 2) Aplique as migrações e rode o pipeline

```bash
.\tasks.ps1 migrate
.\tasks.ps1 run
```

> **Dica (primeira execução, banco vazio):** você pode rodar `.\tasks.ps1 reset-db` (zera o volume e já aplica as migrações).
> **Uso normal:** prefira `.\tasks.ps1 migrate`, porque não apaga dados.

### Reset do banco (apaga os dados)

⚠️ `.\tasks.ps1 reset-db` remove o volume do Postgres (`docker compose down -v`) e apaga todos os dados.

```bash
.\tasks.ps1 reset-db
.\tasks.ps1 run
```

### Comandos úteis

```bash
.\tasks.ps1 check
.\tasks.ps1 logs
```

## Comandos equivalentes (Mac/Linux) — sem `tasks.ps1`

```bash
docker compose up -d
alembic upgrade head
python -m scripts.main
ruff check . && pytest -q
```

### Para reset completo (apaga dados):

```bash
docker compose down -v
docker compose up -d
alembic upgrade head
```

## Como rodar (local, sem Docker)

> Caminho alternativo (best effort). O fluxo recomendado é via Docker.


### 1) Instale as dependências

```bash
pip install -r requirements.txt
```

### 2) Garanta que o PostgreSQL local está rodando e que o `.env` aponta para ele.

### 3) Rode as migrações e o pipeline:

```bash
alembic upgrade head
python -m scripts.main
```

## Como funciona (resumo)

Para cada CSV:

1. Lê linhas (`csv.DictReader`)
2. Normaliza campos (`core/*.py`)
3. Valida dados (`core/*.py`)
4. Se válido: insere no PostgreSQL
5. Se inválido: registra via logging

A contagem **Inseridos no banco** considera apenas inserções novas (duplicatas por `id` não entram).

## Export opcional de inválidos

Por padrão, inválidos são apenas registrados via logging (limitado no console).
Se quiser exportar todos os inválidos para arquivo, habilite no `.env`:

- `EXPORT_INVALIDS=1`
- `INVALIDS_DIR=out/invalids`
- `INVALIDS_FORMAT=csv` (ou `json`)

Ao rodar `.\tasks.ps1 run`, os arquivos serão gerados em `out/invalids/`.

## Observação sobre performance (inserção em lote)

Este projeto insere registros válidos `linha a linha` por simplicidade (volume pequeno).
Em cenários de produção com grandes volumes, a estratégia recomendada seria `bulk insert` (ex.: `COPY` ou batches), reduzindo overhead de round-trips ao banco.

## Licença

Projeto de portfólio.