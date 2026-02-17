# Projeto Cursos (CSV → PostgreSQL)

Projeto de portfólio focado em **Python + validação de dados + carga em PostgreSQL**.  
O objetivo é demonstrar um mini pipeline ETL: leitura de CSV → normalização/validação → inserção no banco.

---

## Status

- [x] Leitura de CSV (`csv.DictReader`)
- [x] Normalização e validação (`core/`)
- [x] Pipeline genérico de carga (`scripts/loader.py`)
- [x] Logging configurável (`LOG_LEVEL`)
- [x] Setup de schema via SQL (`python -m scripts.setup_db`)
- [x] Carga no PostgreSQL (com `ON CONFLICT DO NOTHING`)
- [x] Testes com `pytest`
- [x] Padronização com `ruff` (lint/format)
- [x] CI com GitHub Actions (ruff + pytest)
- [x] Docker básico (PostgreSQL via `docker compose`)

Próximos passos (planejados):
- [ ] Export opcional de inválidos (arquivo)
- [ ] Migrações com Alembic (schema versionado)
- [ ] Makefile para comandos padrão (`make up`, `make run`, etc.)

---

## Estrutura do projeto

- `core/`  
  Regras de **normalização** e **validação** por entidade.
- `data/`  
  Arquivos `.csv` de entrada.
- `db/`  
  Conexão com o PostgreSQL.
- `scripts/`  
  Scripts de setup e carga (ETL).
- `tests/`  
  Testes de normalização e validação.

---

## Requisitos

- Python 3.11+ (recomendado)
- Docker Desktop (recomendado) **ou** PostgreSQL local
- Dependências principais:
  - `psycopg`
  - `python-dotenv`

---

## Configuração (.env)

1) Copie o arquivo de exemplo:

```bash
copy .env.example .env
```

2) Ajuste o `.env` se necessário (principalmente `PGPASSWORD` e `PGDATABASE`).

O projeto lê as variáveis via `config.py`. O `.env` não deve ser commitado (está no `.gitignore`).

## Como rodar (Docker - recomendado)

> **Importante:** execute os comandos a partir da **raiz** do projeto.

### 1) Suba o PostgreSQL (Docker)

```bash
docker compose up -d
docker compose ps
```

### 2) Crie as tabelas e rode o pipeline

⚠️ `scripts.setup_db` executa reset do schema (apaga dados).

```bash
python -m scripts.setup_db
python -m scripts.main
```

### Reset do banco (apaga os dados)

```bash
docker compose down -v
docker compose up -d
python -m scripts.setup_db
```

## Como rodar (local, sem Docker)

### 1) Instale as dependências

```bash
pip install psycopg python-dotenv
```

Garanta que o PostgreSQL local está rodando e que o `.env` aponta para ele.

### 2) Rode o setup e o pipeline

```bash
python -m scripts.setup_db
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

## Licença

Projeto de estudo/portfólio.