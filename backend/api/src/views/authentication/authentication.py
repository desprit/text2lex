"""
Authentication endpoints.
"""
from flask_cors import cross_origin
from flask import request, session, jsonify, Blueprint
from werkzeug.security import check_password_hash

from shared.database import models, db_utils


bp = Blueprint("authentication", __name__)


@bp.route("/login", methods=["POST", "OPTIONS"])
@cross_origin(supports_credentials=True)
def login():
    """
    Process user login.
    """

    print("LOGIN")

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

    session["is_admin"] = existing_user.is_admin
    session["username"] = existing_user.username

    role = "admin" if existing_user.is_admin else "user"
    user = {"role": role, "authToken": "testToken"}

    return jsonify({"success": True, "data": user})


@bp.route("/logout")
@cross_origin(supports_credentials=True)
def logout():
    """
    Logout user.
    """

    session.pop("is_admin", None)
    session.pop("username", None)

    return jsonify({"success": True})
