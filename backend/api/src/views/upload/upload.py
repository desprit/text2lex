"""
Upload endpoints.
"""
import os
import uuid
import json
from typing import Tuple, Union

from rq import Queue
from flask_cors import cross_origin
from flask import request, jsonify, Blueprint

from shared.utils import utils
from shared.database import db_utils
from shared.config import UPLOAD_FOLDER, RQ_NLP_QUEUE_LOW


bp = Blueprint("upload", __name__)


def save_text(req: request) -> Tuple[Union[None, str], Union[None, str]]:
    """
    Extract json text or file from request and save it on disk.
    """

    json_data = req.get_json()
    if json_data:
        if not isinstance(json_data, dict) or "text" not in json_data:
            return (None, "Incorrect text payload")
        text = json_data["text"]
        filename = f"{str(uuid.uuid4())}.txt"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        with open(filepath, "w") as w:
            w.write(text)
            return (filename, None)

    file = req.files["file"]
    if not utils.is_allowed_file(file.filename):
        return (None, "Incorrect extension")

    ext = file.filename.rsplit(".", 1)[1]
    filename = f"{str(uuid.uuid4())}.{ext}"
    file.save(os.path.join(UPLOAD_FOLDER, filename))

    return (filename, None)


def schedule(filename: str, user_id: str) -> str:
    """
    Create NLP task. Return RQ job ID.
    """

    params = {"user_id": user_id, "filename": filename}
    redis_conn = db_utils.get_redis_conn()
    queue = Queue(RQ_NLP_QUEUE_LOW, connection=redis_conn)
    job = queue.enqueue("tasks.analyze", **params)

    return job._id


def add_user_job(job_id, user_id) -> None:
    """
    Save job id to the user jobs array.
    """

    redis_conn = db_utils.get_redis_conn()
    current_jobs = redis_conn.hget(f"users:jobs", user_id)
    current_jobs = json.loads(current_jobs) if current_jobs else []
    new_jobs = list(set([*current_jobs, *[job_id]]))
    redis_conn.hset(f"users:jobs", user_id, json.dumps(new_jobs))


@bp.route("/upload", methods=["POST", "OPTIONS"])
@cross_origin(supports_credentials=True)
def upload():
    """
    Create NLP task for uploaded file.
    """

    # TODO: decorator to check token
    token = request.headers.get("Authorization")

    has_text = bool(request.get_json())
    has_file = request.files and request.files["file"]
    if not has_text and not has_file:
        error = "No text input and no file provided"
        return jsonify({"success": False, "message": error})

    filename, error = save_text(request)
    if error:
        return jsonify({"success": False, "message": error})

    job_id = schedule(filename, token)
    add_user_job(job_id, token)

    return jsonify({"success": True, "data": {"jobId": job_id}})
