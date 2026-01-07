from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Length,EqualTo,Email,DataRequired,ValidationError
from market.models import User
from market import bcrypt

class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Username already exists")

    def validate_email(self, email_to_check):
        email_confirm = User.query.filter_by(email=email_to_check.data).first()
        if email_confirm:
            raise ValidationError("Email already exists")

    username= StringField(label="Username:",validators=[Length(min=2,max=20),DataRequired()])
    email = StringField(label="Email:",validators=[Email(),DataRequired()])
    password = PasswordField(label="Password:",validators=[Length(min=6),DataRequired()])
    confirm_password = PasswordField(label="Confirm Password:",validators=[EqualTo("password"),DataRequired()])
    submit = SubmitField(label="Register")

class LoginForm(FlaskForm):
    username = StringField(label="Username:",validators=[Length(min=2,max=20),DataRequired()])
    password = PasswordField(label="Password:",validators=[Length(min=6),DataRequired()])
    submit = SubmitField(label="Login")

class PurchaseForm(FlaskForm):
    submit = SubmitField(label="Purchase Item")

class SellForm(FlaskForm):
    submit = SubmitField(label="Sell")
