"""
Tests for app.py
"""
import io
import os
import json
import time
import uuid
from typing import Tuple, Dict

from rq import Queue
from rq.registry import FinishedJobRegistry

from views.upload import upload
from shared.database import db_utils
from shared.tests.base import TestsBaseClass
from shared.config import UPLOAD_FOLDER, RQ_NLP_QUEUE_LOW


class MockedFile:
    """
    Is used to mock uploaded file.
    """

    filename: str
    content: io.BytesIO

    def __init__(self, filename: str, payload: bytes):
        self.filename = filename
        self.content = io.BytesIO(payload)

    def save(self, filepath):
        """
        Save file on disk.
        """
        with open(filepath, "wb") as w:
            w.write(self.content.read())


class MockedRequest:
    """
    Is used to mock Flask request.
    """

    json_text: Dict[str, str]
    files: Dict[str, Tuple[bytes, str]]

    def __init__(self):
        self.json_text = {}
        self.files = {}

    def set_json(self, text: str):
        """
        Set value of json_text.
        """
        self.json_text = text

    def get_json(self):
        """
        Return json_text value.
        """
        return self.json_text

    def set_file(self, filename: str, payload: bytes):
        """
        Set value of files.
        """
        file = MockedFile(filename, payload)
        self.files = {"file": file}


class UploadTests(TestsBaseClass):
    """
    Tests for app.py
    """

    def test_01_upload_no_file(self):
        """
        Should return an error.
        """

        response = self.app.post("/v1/api/upload")
        data = json.loads(response.data.decode("utf8"))
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "No text input and no file provided")

    def test_02_upload(self):
        """
        Should return job id.
        """

        text = b"some sample text"
        data = {"file": (io.BytesIO(text), "text.txt")}
        response = self.app.post("/v1/api/upload", data=data)
        data = json.loads(response.data.decode("utf8"))
        self.assertTrue(data["success"])
        self.assertIsInstance(data["data"], dict)
        self.assertTrue("jobId" in data["data"])

    def test_03_upload_wrong_extension(self):
        """
        Should return an error when something went wrong during save_text.
        """

        text = b"some sample text"
        data = {"file": (io.BytesIO(text), "text.jpg")}
        response = self.app.post("/v1/api/upload", data=data)
        data = json.loads(response.data.decode("utf8"))
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Incorrect extension")

    def test_04_schedule(self):
        """
        Should create a task a put in Redis queue.
        """

        redis_conn = db_utils.get_redis_conn()
        job_id = upload.schedule("test", "test")
        time.sleep(1)
        finished = FinishedJobRegistry(RQ_NLP_QUEUE_LOW, connection=redis_conn)
        finished_job_ids = finished.get_job_ids()
        queue = Queue(RQ_NLP_QUEUE_LOW, connection=redis_conn)
        active_job_ids = queue.get_job_ids()
        self.assertTrue(job_id in [*finished_job_ids, *active_job_ids])

    def test_05_save_text_input_wrong_json(self):
        """
        Should throw an error if json payload is of wrong structure.
        """

        request = MockedRequest()
        request.set_json({"some-key": "some text"})
        filename, error = upload.save_text(request)
        self.assertEqual(error, "Incorrect text payload")
        self.assertEqual(filename, None)
        request.set_json("some text")
        filename, error = upload.save_text(request)
        self.assertEqual(error, "Incorrect text payload")
        self.assertEqual(filename, None)

    def test_06_save_text_input_correct_json(self):
        """
        Should save json text as file on disk.
        """

        text = "some text"
        request = MockedRequest()
        request.set_json({"text": text})
        filename, error = upload.save_text(request)
        self.assertEqual(error, None)
        assert os.path.isfile(f"{UPLOAD_FOLDER}/{filename}")
        with open(f"{UPLOAD_FOLDER}/{filename}") as f:
            content = f.read()
            self.assertEqual(content, text)

    def test_07_save_text_input_wrong_file_extension(self):
        """
        Shuld throw an error when extension of the file is wrong.
        """

        body = b"abcdef"
        filename = f"{str(uuid.uuid4())}.doc"
        request = MockedRequest()
        request.set_file(filename, body)
        filename, error = upload.save_text(request)
        self.assertEqual(error, "Incorrect extension")
        self.assertEqual(filename, None)

    def test_08_save_text_input_correct_file(self):
        """
        Should save json text as file on disk.
        """

        body = b"abcdef"
        filename = f"{str(uuid.uuid4())}.txt"
        request = MockedRequest()
        request.set_file(filename, body)
        filename, error = upload.save_text(request)
        self.assertEqual(error, None)
        assert os.path.isfile(f"{UPLOAD_FOLDER}/{filename}")
        with open(f"{UPLOAD_FOLDER}/{filename}") as f:
            content = f.read()
            self.assertEqual(content, body.decode())
