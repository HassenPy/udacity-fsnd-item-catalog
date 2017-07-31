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


category_view = CategoryAPI.as_view('category_api')
catalogApp.add_url_rule('/catalog/category/add/',
                        view_func=category_view, methods=['POST', ])
catalogApp.add_url_rule('/catalog/category/<int:id>/',
                        view_func=category_view, methods=['GET', ])
catalogApp.add_url_rule('/catalog/category/<int:id>/delete/',
                        view_func=category_view, methods=['DELETE', ])
catalogApp.add_url_rule('/catalog/category/<int:id>/edit/',
                        view_func=category_view, methods=['PUT', ])
