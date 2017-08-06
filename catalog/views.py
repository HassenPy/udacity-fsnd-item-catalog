"""Catalog views."""
from flask import Blueprint, render_template, request, redirect, session, abort
from flask_login import login_required
from sqlalchemy.exc import IntegrityError

from app import db

from auth.models import User
from .models import Item, Category

catalogApp = Blueprint('catalogApp', __name__)


@catalogApp.route('/', methods=['GET'])
def home():
    """Render the home page with latest items."""
    categories = Category.query.limit(5).all()
    items = Item.query.order_by(Item.created.desc()).limit(5).all()
    return render_template(
        'home.html',
        categories=categories,
        items=items
    )


@catalogApp.route('/category/', methods=['GET'])
def category_list():
    """Render a list with all the communities."""
    categories = Category.query.all()
    return render_template(
        'categoryList.html',
        categories=categories,
    )


@catalogApp.route('/category/<int:id>/', methods=['GET'])
def category_page(id):
    """Return a community page with paginated picks."""
    category = Category.query.get(id)
    offset = request.args.get('o', 1)
    categories = Category.query.limit(5).all()
    if not category:
        abort(404)

    # check if passed offset is an integer
    try:
        offset = int(offset)
    except ValueError:
        offset = 1

    if category:
        # Fetch paginated category items
        items = Item.query.filter_by(
            category=id
        ).paginate(offset, 10)
        return render_template(
            'category.html',
            category=category,
            items=items,
            categories=categories
        )
    return render_template(
        'category.html',
        category=category,
        items=items,
        categories=categories
    )


@catalogApp.route('/pick/add/', methods=['GET', 'POST'])
@login_required
def item_add():
    """Handle adding a new pick."""
    categories = Category.query.all()
    title = request.form.get('title', '')
    link = request.form.get('link', '')
    category = request.form.get('category', '')
    try:
        category = int(category)
    except ValueError:
        category = ''
    fields = {'title': title, 'link': link, 'category': category}

    if request.method == 'POST':
        # Check if required fields exist in POST values.
        if not (title and link and category):
            return render_template(
                'itemAdd.html',
                fields=fields,
                categories=categories,
                error="all fields are required",
                errors=None
            )

        item = Item(title=title, link=link,
                    category=category, author=session['user_id'])
        if item.is_valid():
            try:
                db.session.add(item)
                db.session.commit()
                return redirect('/')
            except IntegrityError:
                db.session.rollback()
                return render_template(
                    'itemAdd.html',
                    categories=categories,
                    fields=fields,
                    error=None,
                    errors={'title': ['a Pick with same title already exists']}
                )
        return render_template(
            'itemAdd.html',
            categories=categories,
            fields=fields,
            error=None,
            errors=item.errors
        )
    return render_template(
        'itemAdd.html',
        categories=categories,
        fields=fields,
        error=None,
        errors=None
    )


@catalogApp.route('/pick/<int:id>/edit/', methods=['GET', 'POST'])
@login_required
def item_edit(id):
    """Handle editing an existing pick."""
    item = Item.query.get(id)
    if not item:
        abort(404)
    categories = Category.query.all()

    # Check permission
    user_id = session.get('user_id', False)
    if user_id:
        admin = User.query.get(user_id).admin

    if (item.author != user_id) and not admin:
        abort(401)

    if request.method == 'POST':
        # Check if required fields exist in POST values.
        title = request.form.get('title', '')
        link = request.form.get('link', '')
        category = request.form.get('category', '')
        # a little type conversion for template comparison
        try:
            category = int(category)
        except ValueError:
            category = ''

        if not (title and link and category):
            return render_template(
                'itemEdit.html',
                item=item,
                categories=categories,
                error="all fields are required",
                errors=None
            )

        # This is required to prevent automatic flushes
        # This is used since if you post with a non-existant category id
        # you will get a category field insert error on .is_valid() call.
        with db.session.no_autoflush:
            item.title = title
            item.link = link
            item.category = category
            is_valid = item.is_valid()

        if is_valid:
            try:
                db.session.commit()
                return redirect('/')
            except IntegrityError:
                db.session.rollback()
                return render_template(
                    'itemEdit.html',
                    categories=categories,
                    item=item,
                    error=None,
                    errors={'title': ['a Pick with same title already exists']}
                )
        return render_template(
            'itemEdit.html',
            categories=categories,
            item=item,
            error=None,
            errors=item.errors
        )
    return render_template(
        'itemEdit.html',
        categories=categories,
        item=item,
        error=None,
        errors=None
    )


@catalogApp.route('/profile/', methods=['GET'])
@login_required
def user_profile():
    """Render the user profile showing his shared picks."""
    user_id = session['user_id']
    items = Item.query.filter_by(author=user_id).all()
    return render_template(
        'profile.html',
        items=items
    )
