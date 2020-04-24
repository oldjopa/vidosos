from flask import *
import flask
from data import db_session
# from data. import *
from flask import make_response

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
            return jsonify({'id': u_id})
        except:
            pass
    else:
        return jsonify({'error': '306'})
