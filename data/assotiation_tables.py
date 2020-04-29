from flask_login.mixins import *
import sqlalchemy
from .db_session import SqlAlchemyBase
from werkzeug.security import *


own_video_table = sqlalchemy.Table('own_video_association', SqlAlchemyBase.metadata,
    sqlalchemy.Column('user_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('video_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('videos.id'))
)


viewed_video_table = sqlalchemy.Table('viewed_video_association', SqlAlchemyBase.metadata,
    sqlalchemy.Column('user_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('video_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('videos.id'))
)
