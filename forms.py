from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[Length(min=4, max=25,message='Min:4 , max 25 symbols'),
                                                  DataRequired(message='This field is required')])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[Length(min=6,message='Min is 6 symbols'), DataRequired(message='This field is required')])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me', validators=[DataRequired()])
    submit = SubmitField('Login')