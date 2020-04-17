from flask import *
from vidosos.data import db_session
from flask_login.login_manager import *
from flask_login.utils import *
from vidosos.data.forms import *
from vidosos.data.user import User
from vidosos.data.video import Video


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

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
            login=form.login,
            age=form.age,
            gender=form.gender,
            email=form.email
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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/videos.sqlite")
    app.run()


if __name__ == '__main__':
    main()