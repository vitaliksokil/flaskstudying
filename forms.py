from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[Length(min=4, max=25,message='Min:4 , max 25 symbols'),
                                                  DataRequired(message='This field is required'),
                                                  Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Username must have only letters,numbers,dots or underscores')])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[Length(min=6,message='Min is 6 symbols'), DataRequired(message='This field is required')])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me', validators=[DataRequired()])
    submit = SubmitField('Login')