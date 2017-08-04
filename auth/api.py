"""Catalog views."""
from flask import Blueprint, jsonify, make_response

from auth.models import User


authAPI = Blueprint('authAPI', __name__)


@authAPI.route('/api/user/<int:id>/')
def get_user(id):
    """GET Method handler."""
    user = User.query.get(id)
    if user:
        return jsonify({
            'username': user.username,
        })

    message = jsonify({
        'error': 'resource not found.'
    })
    return make_response(message, 404)
