"""Catalog views."""
from flask import Blueprint, jsonify, make_response, session
from flask_login import login_required

from app import db
from auth.models import User

from .models import Category, Item
from .serializers import CategorySerializer, ItemSerializer

catalogAPI = Blueprint('catalogAPI', __name__)


@catalogAPI.route('/api/category/<int:id>/', methods=['GET', ])
def get_category(id):
    """GET Method handler."""
    category = Category.query.get(int(id))

    if category:
        # serialize category with items
        category_serialized = CategorySerializer(category=category).serialize()
        return jsonify(category_serialized)

    message = jsonify({
        'error': 'resource not found.'
    })
    return make_response(message, 404)


@catalogAPI.route('/api/item/<int:id>/', methods=['GET', ])
def get_item(id):
    """GET Method handler."""
    item = Item.query.get(int(id))
    if item:
        serialized = ItemSerializer(item).serialize()
        return jsonify(serialized)

    message = jsonify({
        'error': 'resource not found.'
    })
    return make_response(message, 404)


@catalogAPI.route('/api/item/<int:id>/', methods=['DELETE', ])
@login_required
def delete_item(id):
    """DELETE method handler."""
    item = Item.query.get(int(id))
    user = User.query.get(session['user_id'])

    if item:
        if (user.id != item.author) and (not user.is_admin()):
            message = jsonify({
                "error": "unauthorized action."
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
