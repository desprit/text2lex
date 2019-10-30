"""
Tests for app.py
"""
from shared.utils import utils
from shared.tests.base import TestsBaseClass


class AuthenticationTests(TestsBaseClass):
    """
    Tests for app.py
    """

    def test_login_incorrect_credentials(self):
        """
        Should return login page with flash message.
        """

        response = self.app.post(
            "/api/login", data={"username": "admin", "password": "test"}
        )
        error_msg = "Please check your login details and try again."
        self.assertTrue(
            error_msg in response.data.decode("utf8"),
            "Didn't trigger error on incorrect credentials",
        )

    def test_login_correct_credentials(self):
        """
        Should return scrapers page.
        """

        user = {"username": "test", "password": "test"}
        utils.create_user(user, session=self.session)
        response = self.app.post("/api/login", data=user, follow_redirects=True)
        self.assertTrue(
            "scrapers-section" in response.data.decode("utf8"),
            "Didn't render scrapers page",
        )

    def test_logout(self):
        """
        Should return to login page.
        """

        with self.app.session_transaction() as sess:
            sess["user_id"] = "test"
        response = self.app.get("/api/logout", follow_redirects=True)
        with self.app.session_transaction() as sess:
            self.assertTrue("user_id" not in sess)
        self.assertTrue(
            'form class="login-form"' in response.data.decode("utf8"),
            "Didn't render scrapers page",
        )
