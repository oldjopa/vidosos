from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, PasswordField, IntegerField, FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField('Your name', validators=[DataRequired()],
                       render_kw={"placeholder": "Your name"})
    age = IntegerField('Age', render_kw={"placeholder": "Age"})
    login = StringField('Login', validators=[DataRequired()],
                        render_kw={"placeholder": "Login"})
    email = EmailField('Email', validators=[DataRequired()],
                       render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={"placeholder": "Password"})
    password_again = PasswordField('Repeat Password',
                                   validators=[DataRequired()],
                                   render_kw={"placeholder": "Repeat Password"})
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()],
                        render_kw={"placeholder": "Login"})
    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={"placeholder": "Password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit')


class AddVideo(FlaskForm):
    file = FileField('File', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Upload')
