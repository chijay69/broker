from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FloatField, IntegerField
from wtforms.validators import Length, Email, DataRequired


class ContactForm(FlaskForm):
    First_name = StringField('First Name', validators=[Length(0, 64)])
    Last_name = StringField('Last Name', validators=[Length(0, 64)])
    Email = StringField('Email', validators=[Length(1, 64), Email()])
    Subject = StringField('Subject', validators=[Length(1, 64)])
    Message = TextAreaField('Messages')
    submit = SubmitField('Send Message')


class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    btc_balance = FloatField('BTC BALANCE')
    cash_balance = FloatField('CASH BALANCE')
    level = StringField('Level', validators=[DataRequired()])
    submit = SubmitField('Submit')


class BankForm(FlaskForm):
    name = StringField('Account Name', validators=[DataRequired(), Length(1, 128)])
    bank_name = StringField('BankName', validators=[DataRequired(), Length(1, 128)])
    account_no = IntegerField('Account Number')
    submit = SubmitField('Withdraw')


class Paypal(FlaskForm):
    name = StringField('FullName', validators=[Length(1, 128)])
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    submit = SubmitField('Withdraw')


class BitCoin(FlaskForm):
    name = StringField('FullName', validators=[DataRequired(), Length(1, 128)])
    address = StringField('Address', validators=[DataRequired(), Length(1, 128)])
    submit = SubmitField('Withdraw')

