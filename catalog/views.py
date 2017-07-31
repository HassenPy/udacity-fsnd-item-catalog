"""Catalog views."""
from flask import Blueprint, jsonify, request
from flask.views import MethodView
# from flask_login import login_required

# from app import db
from .models import Category, Item
from .serializers import PaginationSerializer


catalogApp = Blueprint('catalogApp', __name__)


class CategoryAPI(MethodView):
    """MethodView that handles all the category API methods."""

    def get(self, id):
        """GET Method handler."""
        category = Category.query.get(id)
        offset = request.args.get('o', 1)
        try:
            offset = int(offset)
        except ValueError:
            offset = 1

        if category:
            paginated_items = Item.query.paginate(offset, 3)
            paginated_items = PaginationSerializer(paginated_items).serialize()
            return jsonify(paginated_items)

        return jsonify({
            'error': 'item not found.'
        })


category_view = CategoryAPI.as_view('category_api')
catalogApp.add_url_rule('/catalog/category/add/',
                        view_func=category_view, methods=['POST', ])
catalogApp.add_url_rule('/catalog/category/<int:id>/',
                        view_func=category_view, methods=['GET', ])
catalogApp.add_url_rule('/catalog/category/<int:id>/delete/',
                        view_func=category_view, methods=['DELETE', ])
catalogApp.add_url_rule('/catalog/category/<int:id>/edit/',
                        view_func=category_view, methods=['PUT', ])
