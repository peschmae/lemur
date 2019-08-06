"""Adds fulltext search on key certificate fields.

Revision ID: 08f5c15018d9
Revises: 32826ef900e2
Create Date: 2019-07-24 15:05:05.181748

"""

# revision identifiers, used by Alembic.
revision = "08f5c15018d9"
down_revision = "32826ef900e2"

from alembic import op
import sqlalchemy as sa

import sqlalchemy_utils
from sqlalchemy_searchable import sync_trigger


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    conn = op.get_bind()

    op.add_column(
        "certificates",
        sa.Column("search_vector", sqlalchemy_utils.types.ts_vector.TSVectorType(), nullable=True),
    )
    op.create_index(
        "ix_certificates_search_vector",
        "certificates",
        ["search_vector"],
        unique=False,
        postgresql_using="gin",
    )
    sync_trigger(conn, "certificates", "search_vector", ["name", "cn", "description", "owner"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_certificates_search_vector", table_name="certificates")
    op.drop_column("certificates", "search_vector")
    sync_trigger(conn, "certificates", "search_vector", ["name", "cn", "description", "owner"])
    # ### end Alembic commands ###
