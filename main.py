from flask import *
from data import db_session
from flask_login.login_manager import *
from flask_login.utils import *
from data.forms import *
from data.user import User
from data.video import Video


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    return render_template("index.html")


def main():
<<<<<<< Updated upstream
    db_session.global_init("db/blogs.sqlite")
    app.run()
=======
    db_session.global_init("db/videos.sqlite")
    app.register_blueprint(vidosos_api.blueprint)
    app.run(host='0.0.0.0', port='81')
>>>>>>> Stashed changes


if __name__ == '__main__':
    main()
