"""added data update

Revision ID: f009f7ab89df
Revises: 4664efb10f26
Create Date: 2022-03-03 00:36:44.162543

"""
from alembic import op, context
import sqlalchemy as sa
from sqlalchemy import String, Column
from sqlalchemy.sql import table, column
from tests.db_data import *


# revision identifiers, used by Alembic.
revision = 'f009f7ab89df'
down_revision = '4664efb10f26'
branch_labels = None
depends_on = None


def upgrade():
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_upgrades()


def downgrade():
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_downgrades()


def data_upgrades():
    engine = sa.create_engine(
    "sqlite:///./test.db", connect_args={"check_same_thread": False}
    )
    Session = sa.orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = Session(bind=engine.connect())

    db.add_all(get_roles())
    db.commit()

    db.add_all(get_users())
    db.commit()

    db.add_all(get_audit_commisons())
    db.commit()

    #db.add_all(get_audit_commision_users())
    #db.commit()

    db.add_all(get_marks())
    db.commit()

    db.add_all(get_protocols())
    db.commit()

    db.add_all(get_courses())
    db.commit()

    #db.add_all(get_user_courses())
    #db.commit()

    db.add_all(get_schedules())
    db.commit()

    db.add_all(get_audits())
    db.commit()

    db.add_all(get_appeals())
    db.commit()

    db.close()
  

def data_downgrades():
    op.execute("delete from role where 1=1")
    op.execute("delete from user where 1=1")
    op.execute("delete from audit_commission where 1=1")
    op.execute("delete from audit_commission_user where 1=1")
    op.execute("delete from mark where 1=1")
    op.execute("delete from protocol where 1=1")
    op.execute("delete from course where 1=1")
    op.execute("delete from user_course where 1=1")
    op.execute("delete from schedule where 1=1")
    op.execute("delete from audit where 1=1")
    op.execute("delete from appeal where 1=1")
