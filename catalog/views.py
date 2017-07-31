"""Catalog views."""
from flask import Blueprint, jsonify, request, make_response
from flask.views import MethodView
from flask_login import login_required
from sqlalchemy.exc import IntegrityError

from app import db
from auth.utils import is_admin
from .models import Category, Item
from .serializers import CategorySerializer


catalogApp = Blueprint('catalogApp', __name__)


class CategoryAPI(MethodView):
    """MethodView that handles all the category API methods."""

    def get(self, id):
        """GET Method handler."""
        offset = request.args.get('o', 1)

        # Check if passed id is an integer
        try:
            category = Category.query.get(int(id))
        except ValueError:
            message = jsonify({
                'error': 'id parameter must be an integer.'
            })
            return make_response(message, 400)
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
            category_serialized = CategorySerializer(
                title=category.title,
                description=category.description,
                paginator=paginatetor
            ).serialize()
            return jsonify(category_serialized)

        message = jsonify({
            'error': 'item not found.'
        })
        return make_response(message, 404)

    @login_required
    @is_admin
    def post(self):
        """GET Method handler."""
        title = request.form.get('title', '')
        description = request.form.get('description', '')
        if not (title or description):
            return make_response(jsonify({
                'errors': 'missing required parameters'
            }), 400)

        category = Category(title=title, description=description)
        if category.is_valid():
            try:
                db.session.add(category)
                db.session.commit()
                message = jsonify({
                    "message": "category created successfully."
                })
                return make_response(message, 201)
            except IntegrityError:
                message = jsonify({
                    "message": "Category already exists."
                })
                return make_response(message, 409)
        return make_response(jsonify(category.errors), 400)

    @login_required
    @is_admin
    def delete(self, id):
        """DELETE method handler."""
        # Check if passed id is an integer
        try:
            category = Category.query.get(int(id))
        except ValueError:
            message = jsonify({
                'error': 'id parameter must be an integer.'
            })
            return make_response(message, 400)

        if category:
            db.session.delete(category)
            db.session.commit()
            message = jsonify({
                "message": "Category successfully deleted."
            })
            return make_response(message, 200)
        else:
            message = jsonify({
                "message": "Category doesn't exist."
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
                'error': 'missing required parameters.'
            })
            return make_response(message, 400)
        # Check if passed id is an integer
        try:
            category = Category.query.get(int(id))
        except ValueError:
            message = jsonify({
                'error': 'id parameter must be an integer.'
            })
            return make_response(message, 400)

        if category:
            category.title = title
            category.description = description
            print(isinstance(category, Category))
            if category.is_valid():
                db.session.commit()
                message = jsonify({
                    "message": "Category successfully updated."
                })
                return make_response(message, 200)
            return make_response(jsonify(category.errors), 400)
        else:
            message = jsonify({
                "message": "Category doesn't exist."
            })
            return make_response(message, 404)


category_view = CategoryAPI.as_view('category_api')
catalogApp.add_url_rule('/catalog/category/add/',
                        view_func=category_view, methods=['POST', ])
catalogApp.add_url_rule('/catalog/category/<int:id>/',
                        view_func=category_view, methods=['GET', ])
catalogApp.add_url_rule('/catalog/category/<int:id>/',
                        view_func=category_view, methods=['DELETE', ])
catalogApp.add_url_rule('/catalog/category/<int:id>/',
                        view_func=category_view, methods=['PUT', ])
