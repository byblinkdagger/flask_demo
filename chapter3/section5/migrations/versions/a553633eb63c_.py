"""empty message

Revision ID: a553633eb63c
Revises: 
Create Date: 2018-08-20 14:49:44.581064

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a553633eb63c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('login_users')
    op.drop_index('filehash', table_name='pastefile')
    op.drop_table('pastefile')
    op.drop_table('restful_user')
    op.drop_table('users')
    op.drop_table('users2')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users2',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('users',
    sa.Column('Id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('Name', mysql.VARCHAR(length=25), nullable=True),
    sa.PrimaryKeyConstraint('Id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('restful_user',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=128), nullable=False),
    sa.Column('address', mysql.VARCHAR(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('pastefile',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('filename', mysql.VARCHAR(length=5000), nullable=False),
    sa.Column('filehash', mysql.VARCHAR(length=128), nullable=False),
    sa.Column('filemd5', mysql.VARCHAR(length=128), nullable=False),
    sa.Column('uploadtime', mysql.DATETIME(), nullable=False),
    sa.Column('mimetype', mysql.VARCHAR(length=256), nullable=False),
    sa.Column('size', mysql.INTEGER(display_width=11, unsigned=True), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_index('filehash', 'pastefile', ['filehash'], unique=True)
    op.create_table('login_users',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=128), nullable=False),
    sa.Column('login_count', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('last_login_ip', mysql.VARCHAR(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###