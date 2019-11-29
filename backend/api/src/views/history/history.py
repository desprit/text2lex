"""
Upload endpoints.
"""
import json
from typing import Dict, Union, List

from flask_cors import cross_origin
from flask import request, jsonify, Blueprint

from shared.utils import utils
from shared.database import db_utils


bp = Blueprint("history", __name__)
Relics = List[Dict[str, Union[str, int]]]


def create_job_info_object(
    job_status: Dict[str, str],
    job_relics: Relics,
    job_sample: str,
    job_id: str,
    with_relics: bool = True,
):
    """
    Create a job info object from given values.
    """

    job_object = {
        "relics": [],
        "nRelics": len(job_relics),
        "jobId": job_id,
        "success": False,
        "expired": False,
        "inProgress": False,
        "sample": job_sample,
    }
    if job_status:
        job_object["timestamp"] = job_status["timestamp"]
        job_object["success"] = job_status["success"] == "1"
    if with_relics:
        job_object["relics"] = job_relics

    if job_status and job_status["success"] == "0" and not job_relics:
        job_object["inProgress"] = True

    if job_status and job_status["success"] == "1" and not job_relics:
        job_object["expired"] = True

    return job_object


def get_job_info(
    redis_conn, job_id: str, with_relics=True
) -> Dict[str, Union[bool, str]]:
    """
    Pull meta info for a given job from Redis.
    Scenario 1: job status is True, job relics present (ok)
    Scenario 2: job status is None, job relics present (wrong status, fix)
    Scenario 3: job status is True, no job relics (expired)
    Scenario 4: job status is None, no job relics (wrong everything)
    """

    job_status = redis_conn.hget("jobs:status", job_id)
    job_status = json.loads(job_status) if job_status else None
    relics = redis_conn.get(f"relics:{job_id}")
    sample = json.loads(relics)["sample"] if relics else ""
    relics = json.loads(relics)["relics"] if relics else []

    if not job_status and relics:
        job_status = utils.mark_job_success(job_id, True)
    job_object = create_job_info_object(
        job_status, relics, sample, job_id, with_relics=with_relics
    )

    return job_object


def get_user_jobs(redis_conn, user_id: str) -> List[str]:
    """
    Return job ids from Redis for a given user.
    """

    user_jobs = redis_conn.hget("users:jobs", user_id)
    user_jobs = json.loads(user_jobs) if user_jobs else []

    return user_jobs


def get_job(job_id: str):
    """
    Pull meta info for a given job from Redis.
    """

    redis_conn = db_utils.get_redis_conn()
    job_info = get_job_info(redis_conn, job_id, with_relics=False)

    return jsonify({"success": True, "data": job_info})


@bp.route("/history")
@cross_origin(supports_credentials=True)
def get_jobs():
    """
    Pull meta info for a given list of jobs from Redis.
    """

    redis_conn = db_utils.get_redis_conn()
    token = request.headers.get("Authorization")
    job_ids = get_user_jobs(redis_conn, token)
    jobs = [get_job_info(redis_conn, job_id, with_relics=False) for job_id in job_ids]
    jobs = [j for j in jobs if j]

    return jsonify({"success": True, "data": jobs})


@bp.route("/history/<job_id>")
@cross_origin(supports_credentials=True)
def get_relics(job_id: str):
    """
    Get relics for a given job from Redis.
    """

    redis_conn = db_utils.get_redis_conn()
    relics = redis_conn.get(f"relics:{job_id}")
    relics = json.loads(relics)["relics"] if relics else []

    return jsonify({"success": True, "data": relics})
