"""modified datetime to current_timestamp, due to issue with asyncpg

Revision ID: 85713d3155eb
Revises: 2b76acfd702e
Create Date: 2025-03-08 23:42:16.810509

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel



# revision identifiers, used by Alembic.
revision: str = '85713d3155eb'
down_revision: Union[str, None] = '2b76acfd702e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'library', ['book_id'])
    op.create_unique_constraint(None, 'userfine', ['user_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'userfine', type_='unique')
    op.drop_constraint(None, 'library', type_='unique')
    # ### end Alembic commands ###
