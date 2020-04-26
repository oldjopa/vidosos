from flask_login.mixins import *
import sqlalchemy
from .db_session import SqlAlchemyBase
from werkzeug.security import *


class OwnVideo(SqlAlchemyBase, UserMixin):
    __tablename__ = 'OwnVideo'

    user_id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True)
    video_id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True)
