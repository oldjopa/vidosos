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
ALLOWED_EXTENSIONS = ["mp4"]

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_session.global_init('db/videos.sqlite')
    vidosos_api.set_user_id(user_id)
    session = db_session.create_session()
    return session.query(User).get(user_id)


import random   # убрать потом


@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect('/non_authorization')
    session = db_session.create_session()
    all_videos = set(session.query(Video).all())
    user = session.query(User).filter(User.id == current_user.id).first()
    possible_videos = all_videos - set(user.viewed_videos)
    if not possible_videos:
        return redirect('/no_videos')
    random_video = random.choice(list(possible_videos))
    user.viewed_videos.append(random_video)
    session.merge(user)
    session.commit()
    src = f'/static/video/{random_video.filename}'
    vidosos_api.set_video_id(random_video.id)    # скармливаем апи id видео
    return render_template("index.html", src=src)


@app.route('/non_authorization')
def non_authorization():
    return render_template('non_authorization.html')


@app.route('/no_videos')
def no_videos():
    return render_template('no_videos.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('user_reg.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.login == form.login.data).first():
            return render_template('user_reg.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
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
    return render_template('user_reg.html', title='Регистрация', form=form)


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
        return render_template('user_log.html', title='Авторизация',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('user_log.html', title='Авторизация', form=form)


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
                    filename=filename
                )
                user = session.query(User).filter(User.id == current_user.id).first()
                user.own_videos.append(video)
                session.add(video)
                session.merge(user)
                session.commit()
                return redirect('/my_videos')

    return render_template('upload_video.html', form=form,
                           title='Добавление видео')


@app.route('/my_videos')
def get_user_videos():
    #if not current_user.is_authenticated:
        #return redirect('/non_authorization')
    session = db_session.create_session()
    users_videos = session.query(Video).filter(
        (own_video_table.c.user_id == current_user.id)
        & (Video.id == own_video_table.c.video_id)).all()
    video_list = {}
    for video in users_videos:
        name = 'static/video/' + video.filename[:-4] + '.png'
        video_list[video.description] = name
    session.commit()
    return render_template('view_videos.html', title='Мои видео',
                           videos=video_list.items())


@app.route('/favourite_videos')
def get_favourite_videos():
    if not current_user.is_authenticated:
        return redirect('/non_authorization')
    session = db_session.create_session()
    users_videos = session.query(Video).filter(
        (favourite_video_table.c.user_id == current_user.id)
        & (Video.id == favourite_video_table.c.video_id)).all()
    session.commit()
    return render_template('view_videos.html', title='Избранные видео',
                           videos=users_videos)


@app.route('/delete_my_video/<video_id>')
def delete_my_video(video_id):
    if not current_user.is_authenticated:
        return redirect('/non_authorization')
    session = db_session.create_session()
    video = session.query(Video).filter(Video.id == video_id).first()
    if video:
        session.delete(video)
        session.commit()
    else:
        abort(404)
    session.commit()
    return redirect('/my_videos')


@app.route('/delete_favourite_video/<video_id>')
def delete_favourite_video(video_id):
    if not current_user.is_authenticated:
        return redirect('/non_authorization')
    session = db_session.create_session()
    video = session.query(Video).filter(Video.id == video_id).first()
    if video:
        session.delete(video)
        session.commit()
    else:
        abort(404)
    session.commit()
    return redirect('/favourite_videos')


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
