from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, BooleanField
from wtforms.validators import EqualTo, Email, DataRequired, Length, ValidationError

from app.models import User


class RegistrationForm (FlaskForm):
    firstname = StringField ('Firstname', validators=[DataRequired ()])
    lastname = StringField ('Lastname', validators=[DataRequired ()])

    email = StringField ('Email', validators=[DataRequired (), Email ()])
    password = PasswordField ('Password', validators=[DataRequired (), EqualTo('password1', message='Passwords must '
                                                                                                     'match.')])
    password1 = PasswordField ('Confirm password', validators=[DataRequired()])
    phone = IntegerField ('Phone number', validators=[DataRequired()])
    country = StringField ('Country', validators=[DataRequired()])
    submit = SubmitField ('Create Account')

    @staticmethod
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already registered')


class LoginForm (FlaskForm):
    email = StringField ('Your Email', validators=[DataRequired (), Length (1, 64), Email ()])
    password = PasswordField ('Password', validators=[DataRequired ()])
    remember_me = BooleanField ('keep me logged in')
    submit = SubmitField ('Login')


class PasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
