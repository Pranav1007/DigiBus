from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.fields.html5 import DateField
from flaskblog.models import Consumer


class RegistrationForm(FlaskForm):
    fullname = StringField('Fullname', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=18)])
    email = StringField('Email ID',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=18)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=4, max=18), EqualTo('password')])
    submit = SubmitField('Sign Up')
    def validate_username(self, username):
        user = Consumer.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = Consumer.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email Id', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=18)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ContactForm(FlaskForm):
    fullname = StringField('Fullname', validators=[DataRequired()])
    number = StringField('Mobile Number', validators=[DataRequired(), Length(min=10, max=10)])
    email = StringField('Email ID',validators=[DataRequired(), Email()])
    query = TextAreaField('Enter your Query', validators=[DataRequired()])
    submit = SubmitField('Submit')

class PassbookingForm(FlaskForm):
    city = SelectField('City :', validators=[DataRequired()], choices=[("Chennai","Chennai")])
    fromaddress = SelectField('From :', validators=[DataRequired()], choices=[("Potheri","Potheri"),("Kattangulathur","Kattangulathur")])
    toaddress = SelectField('To :', validators=[DataRequired()], choices=[("Tambaram","Tambaram"),("Chennai Egmore","Chennai Egmore")])
    date = DateField('Date :', validators=[DataRequired()])
    pass_type = SelectField('Pass Validity :', validators=[DataRequired()], choices=[("Monthly"),("Quarterly"),("Half-Yearly"),("Annually")])
    submit = SubmitField('Proceed to Payment')

class UpdateAccountForm(FlaskForm):
    fullname = StringField('Fullname', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=18)])
    email = StringField('Email ID',validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')
    def validate_username(self, username):
        if username.data != current_user.username:
            user = Consumer.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
         if email.data != current_user.email:
            user = Consumer.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class PaymentForm(FlaskForm):
    amount = StringField('Amount to be added to wallet :', validators=[DataRequired()])
    cardname = StringField('Name on Card :', validators=[DataRequired()])
    cardnumber = StringField('Card Number :', validators=[DataRequired(), Length(min=16, max=16)])
    expirydate = DateField('Expiry Date :', validators=[DataRequired()])
    cvvnumber = PasswordField('CVV :', validators=[DataRequired(), Length(min=3, max=3)])
    submit = SubmitField('Continue to Checkout')
