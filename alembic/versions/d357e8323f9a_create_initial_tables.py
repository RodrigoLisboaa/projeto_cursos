"""create initial tables

Revision ID: d357e8323f9a
Revises:
Create Date: 2026-02-19 14:03:41.838468

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d357e8323f9a"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # alunos
    op.create_table(
        "alunos",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=False),
        sa.Column("nome", sa.String(length=120), nullable=False),
        sa.Column("email", sa.String(length=150), nullable=False, unique=True),
        sa.Column("idade", sa.Integer(), nullable=False),
        sa.CheckConstraint("idade >= 16", name="ck_alunos_idade_min"),        
    )

    #c ursos
    op.create_table(
        "cursos",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=False),
        sa.Column("nome", sa.String(length=120), nullable=False),
        sa.Column("ativo", sa.Boolean(), nullable=False),
    )

    # matriculas
    op.create_table(
        "matriculas",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=False),
        sa.Column("aluno_id", sa.Integer(), nullable=False),
        sa.Column("curso_id", sa.Integer(), nullable=False),
        sa.Column("data_matricula", sa.Date(), nullable=False),
        sa.ForeignKeyConstraint(["aluno_id"], ["alunos.id"], name="fk_matriculas_alunos"),
        sa.ForeignKeyConstraint(["curso_id"], ["cursos.id"], name="fk_matriculas_cursos"),
        sa.UniqueConstraint("aluno_id", "curso_id", name="uq_aluno_curso"),
    )


def downgrade() -> None:
    op.drop_table("matriculas")
    op.drop_table("cursos")
    op.drop_table("alunos")
