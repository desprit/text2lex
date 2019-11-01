"""
Tests for app.py
"""
import io
import os
import json

from shared.tests.base import TestsBaseClass
from shared.config import UPLOAD_FOLDER


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
        self.assertEqual(data["message"], "No file")

    def test_02_upload_wrong_extension(self):
        """
        Should return an error.
        """

        data = {"file": (io.BytesIO(b"abcdef"), "test.jpg")}
        response = self.app.post("/v1/api/upload", data=data)
        data = json.loads(response.data.decode("utf8"))
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Incorrect extension")

    def test_03_upload_correct_extension(self):
        """
        Should return an error.
        """

        filename = "test.txt"
        file_path = f"{UPLOAD_FOLDER}/{filename}"
        data = {"file": (io.BytesIO(b"abcdef"), filename)}
        response = self.app.post("/v1/api/upload", data=data)
        data = json.loads(response.data.decode("utf8"))
        self.assertTrue(data["success"])
        self.assertTrue(os.path.isfile(file_path))
