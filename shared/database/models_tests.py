"""
Tests for models.py
"""
import re

from shared.database import models
from shared.tests.base import TestsBaseClass


class ModelsTests(TestsBaseClass):
    """
    Tests for models.py
    """

    def test_generate_uuid(self):
        """
        Should return Odd from the database if exists.
        """

        pattern = re.compile(
            "[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"
        )
        uuid = models.generate_uuid()
        self.assertTrue(pattern.match(uuid))

    def test_user_is_active(self):
        """
        Should return True.
        """

        user = models.User()
        self.assertTrue(user.is_active())

    def test_user_is_authenticated(self):
        """
        Should return False.
        """

        user = models.User()
        self.assertFalse(user.is_authenticated())
