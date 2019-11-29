"""
Project shared utilities.
"""
import json
import datetime
from typing import Dict, List, Tuple, Any

from werkzeug.security import generate_password_hash

from shared.database import models, db_utils
from shared.config import ALLOWED_EXTENSIONS


def create_user(user: Dict[str, Any], session=None) -> Tuple[bool, str]:
    """
    Create a new user.
    """

    user_copy = user.copy()
    password_hash = generate_password_hash(user_copy["password"])
    user_copy["password"] = password_hash

    existing_user = db_utils.get_item(
        models.User, filters={"username": user_copy["username"]}, session=session
    )
    if not existing_user:
        db_utils.create_item(models.User, user_copy, session=session)
        return (True, "")

    return (False, "user already exists")


def is_equal(
    item1: Dict[str, str], item2: Dict[str, str], ignore_fileds: List[str] = None
) -> bool:
    """
    Return True if items are equal.
    Example:
    >>> is_equal({"a": "1", "b": "2"}, {"a": "1"})
    False
    >>> is_equal({"a": "1", "b": "2"}, {"a": "1", "b": "2"})
    True
    """

    default_ignore = ["created", "updated"]
    ignore_fileds = [] if not ignore_fileds else ignore_fileds
    ignore_fileds = ignore_fileds + default_ignore
    ignore_fileds = list(set(ignore_fileds))

    for k, v in item1.items():
        if k in ignore_fileds:
            continue
        if item2.get(k) != v:
            return False

    return True


def timestamp_to_dt(ts: str) -> datetime.datetime:
    """
    Return python datetime object from given timestamp.
    """

    ts_as_int = int(ts) / 1000
    ts_as_datetime = datetime.datetime.fromtimestamp(ts_as_int)

    return ts_as_datetime


def dt_to_milliseconds_str(dt: datetime.datetime) -> str:
    """
    Return timestamp str from python datetime object.
    """

    dt_as_str = str(int(dt.strftime("%s")) * 1000)

    return dt_as_str


def is_allowed_file(filename: str) -> bool:
    """
    Return True when given filename is of correct extension.
    """

    return "." in filename and filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS


def json_serial(obj):
    """
    JSON serializer for objects not serializable by default json code.
    """

    if isinstance(obj, datetime.date):
        return obj.isoformat()

    raise TypeError("Type {} not serializable".format(type(obj)))


def mark_job_success(job_id: str, success: bool, redis_conn=None) -> Dict[str, Any]:
    """
    Save status of the current job to Redis.
    """

    if not redis_conn:
        redis_conn = db_utils.get_redis_conn()
    success = "1" if success else "0"
    now = int(datetime.datetime.utcnow().strftime("%s"))
    value = {"success": success, "timestamp": now}
    redis_conn.hset("jobs:status", job_id, json.dumps(value))

    return value
