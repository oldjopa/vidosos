from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, PasswordField, IntegerField, FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField('Your name', validators=[DataRequired()])
    age = IntegerField('Age')
    login = StringField('Login', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat Password', validators=[DataRequired()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit')


class AddVideo(FlaskForm):
    file = FileField('File', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Upload')
