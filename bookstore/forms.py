from datetime import date

from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import (
    DateField, IntegerField, SelectField, StringField, ValidationError, SubmitField, TextAreaField, PasswordField
)
from wtforms.validators import DataRequired, Length, NumberRange, EqualTo, Email

from bookstore.models import Author, Category, Book


class AuthorForm(FlaskForm):

    name = StringField()
    surname = StringField()


class BookForm(FlaskForm):

    def __init__(self, formdata=_Auto, **kwargs):
        super().__init__(formdata=formdata, **kwargs)
        self.author.choices = Author.query.with_entities(Author.id, (Author.name + ' ' + Author.surname)).all()
        self.category.choices = Category.query.with_entities(Category.id, Category.name)

    title = StringField(validators=[DataRequired(), Length(max=128)])
    author = SelectField(validators=[DataRequired()])
    category = SelectField(validators=[DataRequired()])
    rating = IntegerField(validators=[NumberRange(min=1, max=10)])
    publish_date = DateField(validators=[DataRequired()])
    price = IntegerField(validators=[DataRequired()])
    type = SelectField(choices=['Hardcover', 'Paperback'], validators=[DataRequired()])
    description = TextAreaField()


class LoginForm(FlaskForm):
    email = StringField(
        "Email", validators=[Email(message='Enter a valid email'), DataRequired(message="Please Fill This Field")]
    )
    password = PasswordField("Password", validators=[DataRequired(message="Please Fill This Field")])


class RegisterForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired(message="Please Fill This Field")])
    email = StringField("Email", validators=[Email(message="Please enter a valid email address")])
    password = PasswordField("Password", validators=[
        DataRequired(message="Please Fill This Field"),
        EqualTo(fieldname="confirm", message="Your Passwords Do Not Match")
    ])
    confirm = PasswordField("Confirm Password", validators=[DataRequired(message="Please Fill This Field")])
