"""
Tests for app.py
"""
from shared.tests.base import TestsBaseClass


class AppTests(TestsBaseClass):
    """
    Tests for app.py
    """

    def test_main_page(self):
        """
        Should return correct response code.
        """

        response = self.app.get("/login", follow_redirects=True)
        self.assertEqual(response.status_code, 200), "Wrong status code"
