from flask import *
import flask
from data import db_session
# from data. import *
from flask import make_response
from data.video import Video
from data.user import User
from data.assotiation_tables import *

blueprint = flask.Blueprint('jobs_api', __name__, template_folder='templates')

u_id = -1
v_id = -1


def set_user_id(n_id):
    global u_id
    u_id = n_id


def set_video_id(n_id):
    global v_id
    v_id = n_id


@blueprint.route('/api/like', methods=['GET'])
def get_jobs():
    if u_id != -1:
        try:
            session = db_session.create_session()
            users = session.query(User.id).filter(
                (liked_video_table.c.video_id == v_id) & (User.id == liked_video_table.c.user_id)).all()
            if u_id in users:
                # dislike
                return jsonify({'error': 'alresdy_liked'})
            else:
                video = session.query(Video).filter(Video.id == v_id).first()
                video.liked_users.append(session.query(User).filter(User.id == u_id).first())
                session.merge(video)
                session.commit()
                return jsonify({'ok': 'ok'})
        except Exception as e:
            print(e)
            return 'lol'
    else:
        return jsonify({'error': '306'})
