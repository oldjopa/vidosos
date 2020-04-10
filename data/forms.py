from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, PasswordField, IntegerField, FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    login = StringField('Имя пользователя', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    gender = StringField('Имя пользователя', validators=[DataRequired()])
    age = IntegerField(u'Age')
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    login = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class AddVideo(FlaskForm):
    file = FileField()
    description = StringField('описание')
    submit = SubmitField('загрузить')