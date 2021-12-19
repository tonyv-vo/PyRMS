from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField, HiddenField
from wtforms import validators
from wtforms.fields.simple import HiddenField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, NumberRange, InputRequired
from app.models import Account

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    name = StringField('Name', validators=[DataRequired()])
    phone = IntegerField('Phone', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired(), Length(max=128)])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = Account.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address - there is a user with this email already.')

class ReviewForm(FlaskForm):
    rating = IntegerField('Rating', validators=[NumberRange(min=1, max=5, message="Rating must between 1 - 5 (inclusive)")])
    comment = TextAreaField('Comment', validators=[DataRequired(), Length(max=300)])
    store = SelectField('Restaurant Location', coerce=int, validators=[InputRequired()])
    submit = SubmitField('Submit Review')
    
class EditEmployeeForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Name', validators=[DataRequired()])
    phone = IntegerField('Phone', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired(), Length(max=128)])
    position = SelectField('Position', choices=[('cook', 'Cook'), ('manager', 'Manager'), ('driver', 'Delivery Driver'), ('inactive', 'Inactive')])
    wage = IntegerField('Wage', validators=[DataRequired()])
    sin = IntegerField('SIN', validators=[DataRequired()])
    hidden = HiddenField()
    submit = SubmitField('Register')