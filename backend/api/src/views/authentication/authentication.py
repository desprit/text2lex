"""
Authentication endpoints.
"""
from flask_cors import cross_origin
from flask import request, session, jsonify
from werkzeug.security import check_password_hash

from app import app
from shared.database import models, db_utils


@app.route("/api/login", methods=["POST", "OPTIONS"])
@cross_origin(supports_credentials=True)
def login():
    """
    Process user login.
    """

    if request.method == "OPTIONS":
        return jsonify({"status": "success"})

    username = request.json.get("username")
    password = request.json.get("password")
    existing_user: models.User = db_utils.get_item(
        models.User, filters={"username": username}
    )
    if not existing_user or not check_password_hash(existing_user.password, password):
        return jsonify(
            {
                "status": "error",
                "message": "Please check your login details and try again.",
            }
        )

    session["is_admin"] = existing_user.is_admin
    session["username"] = existing_user.username

    role = "admin" if existing_user.is_admin else "user"
    user = {
        "role": role,
        "username": existing_user.username,
        "authToken": "testToken",
    }

    return jsonify({"status": "success", "data": user})


@app.route("/api/logout")
@cross_origin(supports_credentials=True)
def logout():
    """
    Logout user.
    """

    session.pop("is_admin", None)
    session.pop("allowed_scrapers", None)
    session.pop("username", None)

    return jsonify({"status": "success"})
