from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField ,TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class UserUpdateForm(FlaskForm):
    username = StringField('Username')
    email = StringField('Email' ,  validators=[DataRequired(), Email()] )
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    submit = SubmitField('Update')

class AddRecipieForm(FlaskForm):
    title = StringField('Title')
    description = TextAreaField('Description' , render_kw={'rows':4},  validators=[DataRequired()] )
    ingredients = TextAreaField('Ingredients', render_kw={'rows':2} , validators=[DataRequired()])
    instructions = TextAreaField('Instructions',  render_kw={'rows':10} , validators=[DataRequired()])
    tags = StringField('Tags')
    submit = SubmitField('Add New')