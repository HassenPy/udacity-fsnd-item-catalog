"""Catalog views."""
from flask import Blueprint, jsonify, make_response, session
from flask_login import login_required

from app import db
from auth.models import User

from .models import Community, Pick
from .serializers import CommunitySerializer, PickSerializer

catalogAPI = Blueprint("catalogAPI", __name__)


@catalogAPI.route("/api/community/<int:id>/", methods=["GET", ])
def get_community(id):
    """Return a community object based on id."""
    community = Community.query.get(int(id))

    if community:
        # serialize community with picks
        community_serialized = CommunitySerializer(community=community)\
            .serialize()
        return jsonify(community_serialized)

    message = jsonify({
        "error": "resource not found."
    })
    return make_response(message, 404)


@catalogAPI.route("/api/pick/<int:id>/", methods=["GET", ])
def get_pick(id):
    """Return a pick object based on id."""
    pick = Pick.query.get(int(id))
    if pick:
        serialized = PickSerializer(pick).serialize()
        return jsonify(serialized)

    message = jsonify({
        "error": "resource not found."
    })
    return make_response(message, 404)


@catalogAPI.route("/api/pick/<int:id>/", methods=["DELETE", ])
@login_required
def delete_pick(id):
    """Delete a pick object based on id."""
    pick = Pick.query.get(int(id))
    user = User.query.get(session["user_id"])

    if pick:
        # Check if user is the author of the pick.
        if (user.id != pick.author) and (not user.is_admin()):
            message = jsonify({
                "error": "unauthorized action."
            })
            return make_response(message, 401)

        db.session.delete(pick)
        db.session.commit()
        message = jsonify({
            "message": "resource deleted."
        })
        return make_response(message, 200)
    else:
        message = jsonify({
            "error": "resource not found."
        })
        return make_response(message, 404)
