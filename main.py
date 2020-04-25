from flask import *
from data import db_session
from flask_login.login_manager import *
from flask_login.utils import *
from data.forms import *
from data.user import User
from data.video import Video
import vidosos_api

UPLOAD_FOLDER = './videos'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_session.global_init('db/videos.sqlite')
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/')
def index():
    return render_template("index.html")


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
    return render_template('user.html')


@app.route('/my_videos')
def get_user_videos():
    session = db_session.create_session()
    users_videos = session.query(Video).filter(
        (own_video.c.user_id == current_user.id)
        & (Video.id == own_video.c.video_id)).all()
    session.commit()
    return render_template('view_videos.html', title='Мои видео',
                           videos=users_videos)


@app.route('/favourite_videos')
def get_favourite_videos():
    session = db_session.create_session()
    users_videos = session.query(Video).filter(
        (favourite_video.c.user_id == current_user.id)
        & (Video.id == favourite_video.c.video_id)).all()
    session.commit()
    return render_template('view_videos.html', title='Избранные видео',
                           videos=users_videos)


@app.route('/delete_my_video/<video_id>')
def delete_my_video(video_id):
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
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/videos.sqlite")
    app.register_blueprint(vidosos_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()
