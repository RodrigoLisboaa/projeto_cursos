# Projeto Cursos (CSV → PostgreSQL)

Projeto de portfólio focado em **Python + validação de dados + carga em PostgreSQL**.  
O objetivo é demonstrar um mini pipeline ETL: leitura de CSV → normalização/validação → inserção no banco.

---

## Status

- [x] Leitura de CSV (`csv.DictReader`)
- [x] Normalização de dados (`core/`)
- [x] Validação de dados (`core/`)
- [x] Separação entre registros válidos e inválidos (em memória)
- [x] Carga no PostgreSQL (com `ON CONFLICT DO NOTHING`)
- [x] Execução via módulo (`python -m ...`)
- [x] Configuração centralizada via env (`config.py`) + `.env.example`

Próximos passos (planejados):
- [ ] Substituir `print()` por `logging` e gerar resumo do processamento
- [ ] Remover duplicação entre loaders (alunos/cursos) com função genérica
- [ ] Testes com `pytest` (unitários de normalização/validação + fluxo mínimo)
- [ ] Padronização de código (ruff + black)
- [ ] CI básico (GitHub Actions: ruff + pytest)
- [ ] Docker básico (docker-compose com PostgreSQL)
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
  Scripts de carga (ETL).

---

## Requisitos

- Python 3.11+ (recomendado)
- PostgreSQL rodando localmente (por enquanto)
- Dependências:
  - `psycopg` (driver PostgreSQL)
  - `python-dotenv` (carregar variáveis do `.env`)

---

## Configuração (.env)

1) Copie o arquivo de exemplo:

```bash
copy .env.example .env
Ajuste o .env se necessário (principalmente senha e nome do banco).

Exemplo (valores padrão locais):

CSV_DIR=data

PGHOST=localhost
PGPORT=5432
PGDATABASE=mentoria_dev
PGUSER=postgres
PGPASSWORD=

## Como rodar (local)

> **Importante:** execute os comandos a partir da **raiz** do projeto.

### 1) Ativar venv e instalar dependências

Se você já tem o `.venv`, ative e instale:

```bash
pip install psycopg python-dotenv
(Mais adiante isso será substituído por requirements.txt ou pyproject.toml.)

2) Rodar o pipeline
Executa carga de alunos + cursos:

python -m scripts.main
Ou rodar individualmente:

python -m scripts.load_alunos
python -m scripts.load_cursos
Como funciona (resumo)
Para cada CSV:

Lê as linhas do arquivo (csv.DictReader)

Normaliza os campos (core/*.py)

Valida os dados (core/*.py)

Se válido: adiciona na lista de inserção

Se inválido: registra na lista de inválidos

Insere no PostgreSQL usando ON CONFLICT (id) DO NOTHING

Observações
A contagem "Inseridos no banco: X" considera apenas inserções novas.

Se você rodar o script novamente, registros duplicados por id não serão inseridos, e a contagem pode ficar 0.

No estado atual, inválidos são exibidos no console. Em breve será substituído por logging e export opcional.

Licença
Projeto de estudo/portfólio.