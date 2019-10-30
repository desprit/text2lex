"""
Tests for utils.py
"""
import datetime

from shared.utils import utils
from shared.database import models, db_utils
from shared.tests.base import TestsBaseClass


class UtilsTests(TestsBaseClass):
    """
    Tests for utils.py
    """

    def test_01_is_equal_true(self):
        """
        Should return True when items are equal.
        """

        dict1 = {"a": "1", "b": "2"}
        dict2 = {"a": "1", "b": "2"}
        items_equal = utils.is_equal(dict1, dict2)
        self.assertTrue(items_equal)

    def test_02_is_equal_false(self):
        """
        Should return False when items are not equal.
        """

        dict1 = {"a": "1", "b": "2"}
        dict2 = {"a": "1", "b": "3"}
        items_equal = utils.is_equal(dict1, dict2)
        self.assertFalse(items_equal)

    def test_03_is_equal_with_ignore(self):
        """
        Should return False when items are not equal.
        """

        dict1 = {"a": "1", "b": "2"}
        dict2 = {"a": "1", "b": "3"}
        items_equal = utils.is_equal(dict1, dict2, ignore_fileds=["b"])
        self.assertTrue(items_equal)

    def test_04_is_equal_with_ignore_default(self):
        """
        Should return False when items are not equal.
        """

        dict1 = {"a": "1", "created": "2"}
        dict2 = {"a": "1", "created": "3"}
        items_equal = utils.is_equal(dict1, dict2)
        self.assertTrue(items_equal)

    def test_05_timestamp_to_dt(self):
        """
        Should return Python datetime object.
        """

        ts = int(datetime.datetime.utcnow().strftime("%s"))
        ts_object = utils.timestamp_to_dt(ts)
        self.assertIsInstance(ts_object, datetime.datetime)

    def test_06_dt_to_milliseconds_str(self):
        """
        Should return Python datetime object.
        """

        dt = datetime.datetime.utcnow()
        ts = utils.dt_to_milliseconds_str(dt)
        self.assertIsInstance(ts, str)

    def test_07_create_user_exists(self):
        """
        Should return True if user doesn't exist in the database.
        """

        _, user = self.get_random_item(models.User)
        success, error = utils.create_user(user, session=self.session)
        db_user = db_utils.get_item(
            models.User, filters={"id": user["id"]}, session=self.session
        )
        user["password"] = db_user.password
        self.assertTrue(db_user)
        db_user = db_user.as_dict()
        items_equal = utils.is_equal(user, db_user)
        self.assertTrue(items_equal)
        self.assertTrue(success)
        self.assertFalse(error)

    def test_08_create_user_not_exists(self):
        """
        Should return False if user already exists in the database.
        """

        _, user = self.get_random_item(models.User)
        utils.create_user(user, session=self.session)
        success, error = utils.create_user(user, session=self.session)
        self.assertFalse(success)
        self.assertTrue(error)
