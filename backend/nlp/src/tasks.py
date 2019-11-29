"""
Tasks handled by RQ workers.
"""
import os
import json
from typing import Union, List, Dict, Tuple

from rq import get_current_job

from services import dictionary
from shared.utils import utils
from shared.database import db_utils
from shared.config import logger, UPLOAD_FOLDER, RELICS_RESULT_TTL


Relics = List[Dict[str, Union[str, int]]]
Sample = str
Error = Union[str, None]


def check_arguments(user_id: str, filename: str, file_path: str) -> None:
    """
    Check arguments passed to analyze function.
    """

    if not user_id:
        raise ValueError("No user_id provided")
    if not filename:
        raise ValueError("No filename provided")
    if not os.path.isfile(file_path):
        raise ValueError(f"File {file_path} doesn't exist")


def get_text_relics(file_path: str) -> Tuple[Relics, Sample, Error]:
    """
    Return a list of relics for a given text.
    """

    relics = []
    sample = ""
    with open(file_path) as f:
        content = f.read()
        sample = content[:100]
        d = dictionary.process_text(content)
        relics = d.get_relics(sort=True, as_dict=True)

    return (relics, sample, None)


def save_relics(relics: Relics, sample: Sample, job_id: str) -> None:
    """
    Save relics to Redis.
    """

    redis_conn = db_utils.get_redis_conn()
    data = {"relics": relics, "sample": sample}
    redis_conn.setex(f"relics:{job_id}", RELICS_RESULT_TTL, json.dumps(data))


def remove_file(file_path: str) -> None:
    """
    Try to remove processed file.
    """

    try:
        os.remove(file_path)
    except Exception as e:  # pylint: disable=broad-except
        logger.error("Couldn't remove file")
        logger.error(e)


def analyze(user_id: str = None, filename: str = None) -> None:
    """
    Start NLP tasks.
    """

    job = get_current_job()
    job_id = job._id
    file_path = f"{UPLOAD_FOLDER}/{filename}"
    check_arguments(user_id, filename, file_path)
    relics, sample, error = get_text_relics(file_path)
    remove_file(file_path)
    if error:
        utils.mark_job_success(job_id, False)
    else:
        save_relics(relics, sample, job_id)
        utils.mark_job_success(job_id, True)
