"""add new action

Revision ID: 636d44cb7a7c
Revises:
Create Date: 2024-11-15 20:50:19.477580

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '636d44cb7a7c'
down_revision: Union[str, None] = '6093a83228a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('ALTER TABLE plugin_outlook.queue DROP CONSTRAINT ck_queue_valid_enum_action')
    op.execute('ALTER TABLE plugin_outlook.queue ADD CONSTRAINT ck_queue_valid_enum_action CHECK (action IN (1, 2, 3, 4, 5))')


def downgrade() -> None:
    op.execute('ALTER TABLE plugin_outlook.queue DROP CONSTRAINT ck_queue_valid_enum_action')
    op.execute('ALTER TABLE plugin_outlook.queue ADD CONSTRAINT ck_queue_valid_enum_action CHECK (action IN (1, 2, 3, 4))')
