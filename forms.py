from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    fullname = StringField('Fullname', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=18)])
    email = StringField('Email ID',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=18)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=4, max=18), EqualTo('password')])
    submit = SubmitField('Sign In')

class LoginForm(FlaskForm):
    email = StringField('Email Id', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=18)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ContactForm(FlaskForm):
    fullname = StringField('Fullname', validators=[DataRequired()])
    number = StringField('Mobile Number', validators=[DataRequired(), Length(min=10, max=10)])
    email = StringField('Email ID',validators=[DataRequired(), Email()])
    query = StringField('Enter your Query', validators=[DataRequired()])
    remember = BooleanField('Do you have DigiBus Account')
    submit = SubmitField('Submit')

class PassbookingForm(FlaskForm):
    city = StringField('City :', validators=[DataRequired()])
    fromaddress = StringField('From :', validators=[DataRequired()])
    toaddress = StringField('TO :', validators=[DataRequired()])
    busnumber = StringField('Bus Number :', validators=[DataRequired()])
    submit = SubmitField('Proceed to Payment')