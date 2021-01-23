from flask import Blueprint, render_template, redirect, url_for

from bookstore import models
from bookstore import forms

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/')
def books():
    return render_template('books.html', books=models.Book.query)


@main_blueprint.route('/categories')
def categories():
    return render_template('categories.html', categories=models.Category.query)


@main_blueprint.route('/create/author', methods=['GET', 'POST'])
def author_create():
    form = forms.AuthorForm()
    if not form.validate_on_submit():
        return render_template('author_form.html', form=form)
    author = models.Author(
        name=form.name.data,
        surname=form.surname.data
    )
    models.db.session.add(author)
    models.db.session.commit()
    return redirect(url_for('main.books'))


@main_blueprint.route('/create/book', methods=['GET', 'POST'])
def book_create():
    form = forms.BookForm()
    if not form.validate_on_submit():
        return render_template('book_form.html', form=form)
    book = models.Book(
        title=form.title.data,
        author_id=form.author.data,
        category_id=form.category.data,
        rating=form.rating.data,
        publish_date=form.publish_date.data,
        price=form.price.data,
        type=form.type.data,
        description=form.description.data
    )
    models.db.session.add(book)
    models.db.session.commit()
    return redirect(url_for('main.books'))
