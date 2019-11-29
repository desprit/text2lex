"""
Tests for app.py
"""
import json

from shared.utils import utils
from shared.tests.base import TestsBaseClass


class AuthenticationTests(TestsBaseClass):
    """
    Tests for app.py
    """

    def test_login_incorrect_credentials(self):
        """
        Should return an error.
        """

        user = {"username": "admin", "password": "test"}
        response = self.app.post("/v1/api/login", json=user)
        error_msg = "Please check your login details and try again"
        self.assertTrue(
            error_msg in response.data.decode("utf8"),
            "Didn't trigger error on incorrect credentials",
        )

    def test_login_correct_credentials(self):
        """
        Should return success.
        """

        user = {"username": "admin", "password": "admin"}
        utils.create_user(user, session=self.session)
        response = self.app.post("/v1/api/login", json=user, follow_redirects=True)
        data = json.loads(response.data.decode("utf8"))
        self.assertTrue(data["success"])

    def test_logout(self):
        """
        Should remove info from session object.
        """

        response = self.app.get("/v1/api/logout", follow_redirects=True)
        data = json.loads(response.data.decode("utf8"))
        self.assertTrue(data["success"])
