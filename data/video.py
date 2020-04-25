import sqlalchemy
from .db_session import SqlAlchemyBase


class Video(SqlAlchemyBase):
    __tablename__ = 'videos'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    description = sqlalchemy.Column(sqlalchemy.String)
    url = sqlalchemy.Column(sqlalchemy.String)
