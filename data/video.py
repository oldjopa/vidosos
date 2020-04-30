import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Video(SqlAlchemyBase):
    __tablename__ = 'videos'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    description = sqlalchemy.Column(sqlalchemy.String)
    filename = sqlalchemy.Column(sqlalchemy.String)
    owner_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey('users.id'))
    owner = orm.relation('User')
    number_likes = sqlalchemy.Column(sqlalchemy.Integer)
    liked_users = orm.relation('User', secondary='liked_video_association')

