"""Catalog views."""
import json
from flask import Blueprint, render_template, request, redirect, session, abort
from flask_login import login_required

from .models import Item
from .api import CategoryAPI, ItemAPI

catalogApp = Blueprint('catalogApp', __name__)

category_api = CategoryAPI()
item_api = ItemAPI()


@catalogApp.route('/', methods=['GET'])
def home():
    """Display latest items."""
    categories = category_api.get().data.decode('utf-8')
    items = item_api.get().data.decode('utf-8')
    return render_template(
        'home.html',
        categories=json.loads(categories),
        items=json.loads(items)[:10]
    )


@catalogApp.route('/category/', methods=['GET'])
def category_list():
    """GET Method handler."""
    categories = category_api.get().data.decode('utf-8')
    return render_template(
        'categoryList.html',
        categories=json.loads(categories),
    )


@catalogApp.route('/category/<int:id>/', methods=['GET'])
def category_page(id):
    """Category page."""
    category = category_api.get(id).data.decode('utf-8')
    categories = category_api.get().data.decode('utf-8')
    return render_template(
        'category.html',
        category=json.loads(category),
        categories=json.loads(categories)
    )


@catalogApp.route('/item/add/', methods=['GET', 'POST'])
@login_required
def item_add():
    """Add item view."""
    categories = category_api.get().data.decode('utf-8')
    if request.method == 'POST':
        response = item_api.post()
        if response.status_code != 201:
            data = json.loads(response.data.decode('utf-8'))
            error = data.get('error', None)
            errors = data.get('errors', None)
            return render_template(
                'itemAdd.html',
                categories=json.loads(categories),
                error=error,
                errors=errors
            )
        return redirect('/')
    return render_template(
        'itemAdd.html',
        categories=json.loads(categories),
        error=None,
        errors=None
    )


@catalogApp.route('/item/<int:id>/edit/', methods=['GET', 'POST'])
@login_required
def item_edit(id):
    """Edit item view."""
    item = json.loads(item_api.get(id).data.decode('utf-8'))
    categories = json.loads(category_api.get().data.decode('utf-8'))

    if item['author'] != session['user_id']:
        abort(401)

    if request.method == 'POST':
        response = item_api.put(id)
        if response.status_code != 200:
            data = json.loads(response.data.decode('utf-8'))
            print(data)
            error = data.get('error', None)
            errors = data.get('errors', None)
            return render_template(
                'itemEdit.html',
                categories=categories,
                item=item,
                error=error,
                errors=errors
            )
        return redirect('/')
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
    """User profile showing his additions."""
    user_id = session['user_id']
    items = Item.query.filter_by(author=user_id).all()
    return render_template(
        'profile.html',
        items=items
    )
