from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_wtf import FlaskForm
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from sqlalchemy import func
from sqlalchemy.orm import aliased
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_uploads import IMAGES, UploadSet
import click
from werkzeug.utils import secure_filename

from bookstore import models
from bookstore import forms

from werkzeug.security import generate_password_hash, check_password_hash
import random

main_blueprint = Blueprint('main', __name__)
login_manager = LoginManager()
login_manager.login_view = 'main.login'
admin = Admin(template_mode='bootstrap4')
images = UploadSet('images', IMAGES)


def create_roles():
    user_role = models.Role(name='user')
    super_user_role = models.Role(name='superuser')
    models.db.session.add(user_role)
    models.db.session.add(super_user_role)
    models.db.session.commit()
    return


def create_superuser(username, email, password):
    existing_user = models.User.query.filter_by(email=email).first()
    roles = models.Role.query.first()
    if not roles:
        create_roles()
    roles = models.Role.query.filter_by(name='superuser').first()
    if existing_user is None:
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = models.User(
            username=username,
            email=email,
            password=hashed_password,
        )
        models.db.session.add(new_user)
        models.db.session.commit()
        models.db.session.execute(models.roles_users.insert().values(user_id=new_user.id, role_id=roles.id))
        models.db.session.commit()
    else:
        click.echo('A user already exist!')
    return


class AdminModelView(ModelView):

    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('superuser')
                )

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                abort(403)
            else:
                return redirect(url_for('security.login', next=request.url))


admin.add_view(AdminModelView(models.User, models.db.session))
admin.add_view(AdminModelView(models.Role, models.db.session))
admin.add_view(AdminModelView(models.Book, models.db.session))
admin.add_view(AdminModelView(models.Author, models.db.session))
admin.add_view(AdminModelView(models.Category, models.db.session))


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(user_id)


@main_blueprint.route('/')
def books():
    return render_template('books.html', books=models.Book.query, title='Books')


@main_blueprint.route('/categories')
def categories():
    return render_template('categories.html', categories=models.Category.query)


@main_blueprint.route('/categories/<category_id>')
def go_to_category(category_id):
    return render_template(
        'books.html',
        books=models.Book.query.filter_by(category_id=category_id).all(),
        title=models.Category.query.filter_by(id=category_id).one().name
    )


@main_blueprint.route('/create/author', methods=['GET', 'POST'])
@login_required
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
    flash(f'You have added new author {author.name} {author.surname}!')
    return redirect(url_for('main.books'))


@main_blueprint.route('/create/book', methods=['GET', 'POST'])
@login_required
def book_create():
    form = forms.BookForm()
    if not form.validate_on_submit():
        return render_template('book_form.html', form=form)
    uploaded_file = form.cover.data
    filename = secure_filename(uploaded_file.filename)
    book = models.Book(
        title=form.title.data,
        author_id=form.author.data,
        category_id=form.category.data,
        rating=form.rating.data,
        publish_date=form.publish_date.data,
        price=form.price.data,
        type=form.type.data,
        description=form.description.data,
        cover='/static/media/' + filename
    )
    models.db.session.add(book)
    if uploaded_file:
        images.save(form.cover.data)
    models.db.session.commit()
    flash(f'You have added new book {book.title}!')
    return redirect(url_for('main.books'))


@main_blueprint.route('/update/book/<book_id>', methods=['GET', 'POST'])
@login_required
def book_update(book_id):
    book = models.Book.query.get(book_id)
    form = forms.BookForm(obj=book)
    if not form.validate_on_submit():
        return render_template('book_form.html', form=form)
    uploaded_file = form.cover.data
    filename = secure_filename(uploaded_file.filename)
    book.title = form.title.data
    book.author_id = form.author.data
    book.category_id = form.category.data
    book.rating = form.rating.data
    book.publish_date = form.publish_date.data
    book.price = form.price.data
    book.type = form.type.data
    book.description = form.description.data
    if uploaded_file:
        book.cover = '/static/media/' + filename
        images.save(form.cover.data)
    models.db.session.add(book)
    models.db.session.commit()
    flash(f'You have updated {book.title}!')
    return redirect(url_for('main.books'))


@main_blueprint.route('/delete/book/<book_id>', methods=['GET', 'POST'])
@login_required
def book_delete(book_id):
    book = models.Book.query.get(book_id)
    form = FlaskForm()
    if not form.validate_on_submit():
        context = {'form': form, 'title': book.title}
        return render_template('book_delete.html', **context)
    models.db.session.delete(book)
    models.db.session.commit()
    flash(f'You have deleted {book.title}!')
    return redirect(url_for('main.books'))


@main_blueprint.route('/detail/book/<book_id>', methods=['GET'])
def book_detail(book_id):
    book = models.Book.query.get(book_id)
    context = {'book': book}
    return render_template('book_detail.html', **context)


@main_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegisterForm(request.form)
    if not form.validate_on_submit():
        return render_template('register.html', form=form)
    existing_user = models.User.query.filter_by(email=form.email.data).first()
    roles = models.Role.query.first()
    if not roles:
        create_roles()
    roles = models.Role.query.filter_by(name='user').first()
    if existing_user is None:
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = models.User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
        )
        models.db.session.add(new_user)
        models.db.session.commit()
        models.db.session.execute(models.roles_users.insert().values(user_id=new_user.id, role_id=roles.id))
        models.db.session.commit()
        flash('You have successfully registered!')
    else:
        flash('A user already exists.')
        return render_template('register.html', form=form)
    return redirect(url_for('main.books'))


@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if not form.validate_on_submit():
        return render_template('login.html', form=form)
    user = models.User.query.filter_by(email=form.email.data).first()
    if user:
        if check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            flash('You have successfully logged in.')
            return redirect(next_page or url_for('main.books'))
    flash('Invalid username/password combination')
    return redirect(url_for('main.login'))


@main_blueprint.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('You have successfully logged out.')
    return redirect(url_for('main.books'))


@main_blueprint.route('/profile', methods=['GET'])
@login_required
def profile():
    context = {'current_user': current_user,
               'previous_orders': models.Order.query.filter_by(status='Created', user_id=current_user.id).all()}
    return render_template('profile.html', **context)


@main_blueprint.route('/profile/personal_data', methods=['GET'])
@login_required
def user_personal_data():
    context = {'personal_data': models.PersonalData.query.filter_by(user_id=current_user.id).all()}
    return render_template('personal_data.html', **context)


@main_blueprint.route('/cart/book/<book_id>', methods=['GET', 'POST'])
@login_required
def add_to_cart(book_id):
    user_cart = models.Order.query.filter_by(status='Cart', user_id=current_user.id).first()
    if not user_cart:
        order_number = str(random.randint(100000000000, 999999999999))
    else:
        order_number = user_cart.order_number
    order = models.Order(
        order_number=order_number,
        user_id=int(current_user.id),
        book_id=int(book_id),
        status='Cart'
    )
    models.db.session.add(order)
    models.db.session.commit()
    flash('You have made new order.')
    return redirect(url_for('main.books'))


@main_blueprint.route('/cart/<order_id>', methods=['GET', 'POST'])
@login_required
def delete_from_cart(order_id):
    order = models.Order.query.get(order_id)
    title = order.book.title
    models.db.session.delete(order)
    models.db.session.commit()
    flash(f'You have deleted {title}!')
    return redirect(url_for('main.cart'))


@main_blueprint.route('/cart', methods=['GET'])
@login_required
def cart():
    user_cart = models.Order.query.filter_by(status='Cart', user_id=current_user.id).all()
    total_price = models.db.session().query(func.sum(models.Book.price))\
        .join(aliased(models.Order))\
        .filter_by(status='Cart', user_id=current_user.id).first()[0]
    context = {'user_cart': user_cart,
               'total_price': str(total_price)}
    return render_template('cart.html', **context)


@main_blueprint.route('/cart/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    user_cart = models.Order.query.filter_by(status='Cart', user_id=current_user.id).all()
    if user_cart:
        for item in user_cart:
            item.status = 'Created'
        models.db.session.commit()
    else:
        flash('Cart is empty')
    return redirect(url_for('main.cart'))
