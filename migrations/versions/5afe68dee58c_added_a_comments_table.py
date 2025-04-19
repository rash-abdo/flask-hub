"""added a comments table

Revision ID: 5afe68dee58c
Revises: 363cbf7f5185
Create Date: 2025-04-19 12:03:28.575343

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5afe68dee58c'
down_revision = '363cbf7f5185'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('blog_id', sa.Integer(), nullable=True),
    sa.Column('comment', sa.String(length=300), nullable=False),
    sa.ForeignKeyConstraint(['blog_id'], ['blogs.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('blogs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('comments', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blogs', schema=None) as batch_op:
        batch_op.drop_column('comments')

    op.drop_table('comments')
    # ### end Alembic commands ###
