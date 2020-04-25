from flask_login.mixins import *
import sqlalchemy
from .db_session import SqlAlchemyBase
from werkzeug.security import *
from sqlalchemy import orm


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    age = sqlalchemy.Column(sqlalchemy.Integer)
    gender = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String)
    role = sqlalchemy.Integer
    own_videos = orm.relation("Video", secondary="own_video_association")
    favourite_videos = orm.relation("Video",
                                    secondary="favourite_video_association")
    viewed_videos = orm.relation("Video",
                                 secondary="viewed_video_association")

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
