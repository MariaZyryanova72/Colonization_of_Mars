import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Category(SqlAlchemyBase):
    __tablename__ = 'category'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    hazard_category = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    jobs = orm.relation("Jobs", back_populates='user')