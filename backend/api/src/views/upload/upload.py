"""
Upload endpoints.
"""
import os

from flask_cors import cross_origin
from flask import request, jsonify, Blueprint
from werkzeug.utils import secure_filename

from shared.config import UPLOAD_FOLDER
from shared.utils import utils


bp = Blueprint("upload", __name__)


def schedule(filename: str) -> None:
    """
    Create NLP task.
    """

    return True


@bp.route("/upload", methods=["POST", "OPTIONS"])
@cross_origin(supports_credentials=True)
def upload():
    """
    Process user login.
    """

    if not request.files or not request.files["file"]:
        return jsonify({"success": False, "message": "No file"})

    file = request.files["file"]
    if not utils.is_allowed_file(file.filename):
        return jsonify({"success": False, "message": "Incorrect extension"})

    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    # schedule(filename)

    return jsonify({"success": True})
