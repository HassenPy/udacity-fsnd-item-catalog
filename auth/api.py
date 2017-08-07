"""Catalog views."""
from flask import Blueprint, jsonify, make_response, request

from app import db
from auth.models import User

from .utils import get_fb_user

authAPI = Blueprint("authAPI", __name__)


@authAPI.route("/api/user/<int:id>/", methods=["GET"])
def get_user(id):
    """Endpoint to return a user's username from his id."""
    user = User.query.get(id)
    if user:
        return jsonify({
            "username": user.username,
        })

    message = jsonify({
        "error": "resource not found"
    })
    return make_response(message, 404)


@authAPI.route("/fbsignup", methods=["POST"])
def fbsignup():
    """Endpoint to signup using facebook."""
    access_token = request.form["access_token"]

    # Get the user data.
    fb_user = get_fb_user(access_token)

    # Check if username, email, fbid are already used.
    user_fbid = User.query.filter_by(fb_id=fb_user["id"]).first()
    user_name = User.query.filter_by(username=fb_user["name"]).first()
    user_email = User.query.filter_by(email=fb_user["email"]).first()
    if user_fbid:
        return make_response(jsonify({
            "message": "An account associated with your facebook "
                       "account already exists"
        }), 409)
    if user_email:
        return make_response(jsonify({
            "message": "An account with the email associated with your "
                       "facebook account is already used."
        }), 409)

    # use the email if the username is taken
    if user_name:
        username = fb_user["email"]
    else:
        username = fb_user["name"]
    user = User(
        username=username,
        email=fb_user["email"],
        fb_id=fb_user["id"]
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({
        "message": "You are now a member of the Picky community!"
    })
