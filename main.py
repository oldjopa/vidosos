from flask import *
from data import db_session
from flask_login.login_manager import *
from flask_login.utils import *
from data.forms import *
from data.user import User
from data.video import Video
from data.assotiation_tables import *
import vidosos_api
from get_pic import get_pic
from hash_name import *

from werkzeug.utils import secure_filename
import os

import hashlib

UPLOAD_FOLDER = "/static/video"

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static\\video')
ALLOWED_EXTENSIONS = ["mp4", 'MP4']

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_session.global_init('db/videos.sqlite')
    vidosos_api.set_user_id(user_id)
    session = db_session.create_session()
    return session.query(User).get(user_id)


import random  # убрать потом


@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect('/non_authorization')
    session = db_session.create_session()
    all_videos = set(session.query(Video).all())
    user = session.query(User).filter(User.id == current_user.id).first()
    possible_videos = all_videos - set(user.viewed_videos)
    if not possible_videos:
        return render_template('abnormal_situation.html',
                               message="Unfortunately, there are no more videos to watch,"
                                       " but don't worry, there will be new ones soon.")
    random_video = random.choice(list(possible_videos))
    user.viewed_videos.append(random_video)
    session.merge(user)
    session.commit()
    src = f'/static/video/{random_video.filename}'
    vidosos_api.set_video_id(random_video.id)  # скармливаем апи id видео
    return render_template("index.html", src=src, description=random_video.description,
                           like_number=len(random_video.liked_users))


@app.route('/non_authorization')
def non_authorization():
    return render_template('abnormal_situation.html',
                           message="You are not logged in. Register or log in.")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('user_reg.html', title='Registration',
                                   form=form,
                                   message="Passwords are not the same")
        session = db_session.create_session()
        if session.query(User).filter(User.login == form.login.data).first():
            return render_template('user_reg.html', title='Registration',
                                   form=form,
                                   message="This user already exists")
        user = User(
            login=form.login.data,
            age=form.age.data,
            gender=form.gender.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('user_reg.html', title='Registration', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.login == form.login.data).first()
        session.commit()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('user_log.html', title='Authorization',
                               message="Wrong login or password",
                               form=form)
    return render_template('user_log.html', title='Authorization', form=form)


@app.route('/profile')
def profile():
    if not current_user.is_authenticated:
        return redirect('/non_authorization')
    return render_template('user.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/add_video', methods=['GET', 'POST'])
def add_video():
    if not current_user.is_authenticated:
        return redirect('/non_authorization')
    form = AddVideo()
    if request.method == 'POST':
        if form.validate_on_submit():
            file = form.file.data
            if file and allowed_file(file.filename):
                filename = hash_password(file.filename) + '.mp4'
                path_video = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(path_video)
                get_pic(path_video)
                session = db_session.create_session()
                video = Video(
                    description=form.description.data,
                    filename=filename,
                    owner_id=current_user.id,
                    # number_likes=0
                )
                user = session.query(User).filter(User.id == current_user.id).first()
                user.own_videos.append(video)
                video.owner = user
                video.owner_id = user.id
                session.add(video)
                session.merge(user)
                session.commit()
                return redirect('/my_videos/0')
            elif file and not allowed_file(file.filename):
                return render_template('upload_video.html', form=form, title='Uploading video',
                                       message="Sorry, the project only supports videos in mp4 format")

    return render_template('upload_video.html', form=form,
                           title='Uploading video')


@app.route('/my_videos/<video_id>', methods=['GET'])
def get_user_videos(video_id=None):
    if not current_user.is_authenticated:
        return redirect('/non_authorization')
    session = db_session.create_session()
    user = session.query(User).filter(User.id == current_user.id).first()
    users_videos = session.query(Video).filter(
        (own_video_table.c.user_id == user.id)
        & (Video.id == own_video_table.c.video_id)).all()
    if not users_videos:
        return render_template('abnormal_situation.html',
                               message="You don't have a video yet. Add them soon!")
    try:
        video = user.own_videos[int(video_id)]
    except Exception:
        return render_template('abnormal_situation.html',
                               message='Video not found')
    src = f'../static/video/{video.filename}'
    video_list = list()
    for i, video in enumerate(users_videos):
        name = '../static/video/' + video.filename[:-4] + '.png'
        desc = video.description
        if len(desc) > 60:
            desc = desc[:57] + '...'
        video_list.append((i, desc, name))
    session.commit()
    return render_template('view_videos.html', src=src, title='My videos',
                           videos=video_list)


@app.route('edit_video/<video_id>')
def edit_video(video_id):
    pass


@app.route('/delete_my_video/<video_id>')
def delete_my_video(video_id):
    if not current_user.is_authenticated:
        return redirect('/non_authorization')
    session = db_session.create_session()
    video = session.query(Video).filter(Video.id == video_id).first()
    user = video.owner
    if video:
        user.own_videos.remove(video)
        session.delete(video)
        session.commit()
    else:
        return render_template('abnormal_situation.html', message="Video not found.")
    session.commit()
    return redirect('/my_videos/0')


@app.route('/logout')
@login_required
def logout():
    if not current_user.is_authenticated:
        return redirect('/non_authorization')
    logout_user()
    vidosos_api.set_user_id(-1)
    return redirect("/")


def main():
    db_session.global_init("db/videos.sqlite")
    app.register_blueprint(vidosos_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()
