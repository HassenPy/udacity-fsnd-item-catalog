"""Catalog views."""
from flask import Blueprint, jsonify, request, make_response, session
from flask.views import MethodView
from flask_login import login_required
from sqlalchemy.exc import IntegrityError

from app import db
from auth.models import User
from auth.utils import is_admin

from .models import Category, Item
from .serializers import CategoryPageSerializer, CategoryListSerializer, \
                         ItemSerializer, ItemListSerializer

catalogApp = Blueprint('catalogApp', __name__)


class CategoryAPI(MethodView):
    """MethodView that handles all the category API methods."""

    def get(self, id=None):
        """GET Method handler."""
        # If not providing id, return all categories.
        if not id:
            categories = Category.query.all()
            serialized = CategoryListSerializer(categories).serialize()
            return jsonify(serialized)

        # get the pagination offset GET parameter.
        offset = request.args.get('o', 1)
        category = Category.query.get(int(id))

        # check if passed offset is an integer
        try:
            offset = int(offset)
        except ValueError:
            message = jsonify({
                'error': 'offset parameter must be an integer.'
            })
            return make_response(message, 400)

        if category:
            # Fetch paginated category items
            paginatetor = Item.query.filter_by(
                category=id
            ).paginate(offset, 3)

            # serialize category with items
            category_serialized = CategoryPageSerializer(
                title=category.title,
                description=category.description,
                paginator=paginatetor
            ).serialize()
            return jsonify(category_serialized)

        message = jsonify({
            'error': 'resource not found.'
        })
        return make_response(message, 404)

    @login_required
    @is_admin
    def post(self):
        """POST Method handler."""
        # Check if title and description exist in POST values.
        title = request.form.get('title', '')
        description = request.form.get('description', '')
        if not (title and description):
            return make_response(jsonify({
                'errors': 'missing required parameter'
            }), 400)

        category = Category(title=title, description=description)
        if category.is_valid():
            try:
                db.session.add(category)
                db.session.commit()
                message = jsonify({
                    "message": "resource created."
                })
                return make_response(message, 201)
            except IntegrityError:
                message = jsonify({
                    "message": "resouce already exists."
                })
                return make_response(message, 409)
        return make_response(jsonify(category.errors), 400)

    @login_required
    @is_admin
    def delete(self, id):
        """DELETE method handler."""
        category = Category.query.get(int(id))
        if category:
            db.session.delete(category)
            db.session.commit()
            message = jsonify({
                "message": "resource deleted."
            })
            return make_response(message, 200)
        else:
            message = jsonify({
                'error': 'resource not found.'
            })
            return make_response(message, 404)

    @login_required
    @is_admin
    def put(self, id):
        """PUT method handler."""
        title = request.form.get('title', '')
        description = request.form.get('description', '')
        if not (title or description):
            message = jsonify({
                'error': 'missing required parameter.'
            })
            return make_response(message, 400)

        category = Category.query.get(int(id))
        if category:
            category.title = title
            category.description = description
            if category.is_valid():
                db.session.commit()
                message = jsonify({
                    "message": "resource updated."
                })
                return make_response(message, 200)
            return make_response(jsonify(category.errors), 400)
        else:
            message = jsonify({
                "message": "resource doesn't exist."
            })
            return make_response(message, 404)


class ItemAPI(MethodView):
    """MethodView that handles all the Item API methods."""

    def get(self, id=None):
        """GET Method handler."""
        # If not providing id, return all categories.
        if not id:
            items = db.session.query(Item).order_by(Item.created).all()
            serialized = ItemListSerializer(items).serialize()
            return jsonify(serialized)

        item = Item.query.get(int(id))
        if item:
            serialized = ItemSerializer(item).serialize()
            return jsonify(serialized)

        message = jsonify({
            'error': 'resource not found.'
        })
        return make_response(message, 404)

    @login_required
    def post(self):
        """POST Method handler."""
        # Check if required fields exist in POST values.
        title = request.form.get('title', '')
        link = request.form.get('link', '')
        category = request.form.get('category', '')
        if not (title and link and category):
            return make_response(jsonify({
                'errors': 'missing required parameter'
            }), 400)

        item = Item(title=title, link=link,
                    category=category, author=session['user_id'])
        if item.is_valid():
            try:
                db.session.add(item)
                db.session.commit()
                message = jsonify({
                    "message": "resource created."
                })
                return make_response(message, 201)
            except IntegrityError:
                message = jsonify({
                    "message": "resouce already exists."
                })
                return make_response(message, 409)
        return make_response(jsonify(item.errors), 400)

    @login_required
    def delete(self, id):
        """DELETE method handler."""
        item = Item.query.get(int(id))
        user = User.query.get(session['user_id'])

        if item:
            if (user.id != item.author) and (not user.is_admin()):
                message = jsonify({
                    "message": "unauthorized action."
                })
                return make_response(message, 401)

            db.session.delete(item)
            db.session.commit()
            message = jsonify({
                "message": "resource deleted."
            })
            return make_response(message, 200)
        else:
            message = jsonify({
                'error': 'resource not found.'
            })
            return make_response(message, 404)

    @login_required
    def put(self, id):
        """PUT method handler."""
        item = Item.query.get(int(id))
        user = User.query.get(session['user_id'])
        if (user.id != item.author) and (not user.is_admin()):
            message = jsonify({
                "message": "unauthorized action."
            })
            return make_response(message, 401)

        title = request.form.get('title', '')
        link = request.form.get('link', '')
        category = request.form.get('category', '')
        if not (title or link or category):
            message = jsonify({
                'error': 'missing required parameter.'
            })
            return make_response(message, 400)

        if item:
            item.title = title or item.title
            item.link = link or item.link
            item.category = category or item.category
            if item.is_valid():
                db.session.commit()
                message = jsonify({
                    "message": "resource updated."
                })
                return make_response(message, 200)
            return make_response(jsonify(category.errors), 400)
        else:
            message = jsonify({
                "message": "resource doesn't exist."
            })
            return make_response(message, 404)


category_view = CategoryAPI.as_view('category_api')
catalogApp.add_url_rule('/catalog/category/',
                        view_func=category_view, methods=['GET', ])
catalogApp.add_url_rule('/catalog/category/<int:id>/',
                        view_func=category_view, methods=['GET', ])
catalogApp.add_url_rule('/catalog/category/',
                        view_func=category_view, methods=['POST', ])
catalogApp.add_url_rule('/catalog/category/<int:id>/',
                        view_func=category_view, methods=['DELETE', ])
catalogApp.add_url_rule('/catalog/category/<int:id>/',
                        view_func=category_view, methods=['PUT', ])

item_view = ItemAPI.as_view('item_api')
catalogApp.add_url_rule('/catalog/item/',
                        view_func=item_view, methods=['GET', ])
catalogApp.add_url_rule('/catalog/item/<int:id>/',
                        view_func=item_view, methods=['GET', ])
catalogApp.add_url_rule('/catalog/item/',
                        view_func=item_view, methods=['POST', ])
catalogApp.add_url_rule('/catalog/item/<int:id>/',
                        view_func=item_view, methods=['DELETE', ])
catalogApp.add_url_rule('/catalog/item/<int:id>/',
                        view_func=item_view, methods=['PUT', ])
