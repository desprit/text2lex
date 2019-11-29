"""
Authentication endpoints.
"""
from flask_cors import cross_origin
from flask import request, jsonify, Blueprint
from werkzeug.security import check_password_hash

from shared.database import models, db_utils


bp = Blueprint("authentication", __name__)


@bp.route("/login", methods=["POST", "OPTIONS"])
@cross_origin(supports_credentials=True)
def login():
    """
    Process user login.
    """

    # TODO: create token and save user details to Redis

    username = request.json.get("username")
    password = request.json.get("password")
    existing_user: models.User = db_utils.get_item(
        models.User, filters={"username": username}
    )
    if not existing_user or not check_password_hash(existing_user.password, password):
        return jsonify(
            {
                "success": False,
                "message": "Please check your login details and try again",
            }
        )

    role = "admin" if existing_user.is_admin else "user"
    user = {"role": role, "authToken": "testToken"}

    return jsonify({"success": True, "data": user})


@bp.route("/logout")
@cross_origin(supports_credentials=True)
def logout():
    """
    Logout user.
    """

    # TODO: remove user details from Redis for a given token

    return jsonify({"success": True})
