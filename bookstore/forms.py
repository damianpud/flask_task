from datetime import date

from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import (
    DateField, IntegerField, SelectField, StringField, ValidationError, SubmitField, TextAreaField, PasswordField
)
from wtforms.validators import DataRequired, Length, NumberRange

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
    email = StringField("Email", validators=[Length(min=7, max=50), DataRequired(message="Please Fill This Field")])
    password = PasswordField("Password", validators=[DataRequired(message="Please Fill This Field")])
