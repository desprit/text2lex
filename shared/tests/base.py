"""
Tests for app.py
"""
import random
import unittest
from typing import Dict, Tuple, Any

from mixer.backend.sqlalchemy import Mixer

from app import app
from shared.database import db_utils, models


app.config["TESTING"] = True


def load_user(user_id):
    """
    Return user from the database by id.
    """

    db_user = db_utils.get_item(models.User, filters={"id": user_id})

    return db_user


class TestsBaseClass(unittest.TestCase):
    """
    Tests for app.py
    """

    @classmethod
    def setUpClass(cls):
        """
        Methods to be executed once before all tests.
        """

        cls.conn = db_utils.get_postgres_conn()
        cls.redis_conn = db_utils.get_redis_conn(db=1)
        cls.session = db_utils.get_postgres_session(cls.conn)
        cls.mixer = Mixer(session=cls.session, commit=False)
        db_utils.init_db()

    def setUp(self):
        """
        Methods to be executed before every test.
        """

        app.config["TESTING"] = True
        self.app = app.test_client()

    @classmethod
    def tearDownClass(cls):
        """
        Methods to be executed once after all tests.
        """

        cls.session.close()

    def tearDown(self):
        """
        Methods to be executed after every test.
        """

        self.truncate_db()

    # pylint: disable=no-self-use
    def truncate_db(self):
        """
        Remove content from all tables.
        """

        db_utils.truncate_db()
        self.redis_conn.flushdb()

    def get_random_item(
        self, model: models.ProjectModel = None, no_fk: bool = True
    ) -> Tuple[models.ProjectModel, Dict[str, Any]]:
        """
        Generate a fake database item.
        """

        if model:
            obj = self.mixer.blend(model)
        else:
            all_models = db_utils.get_models()
            if no_fk:
                all_models = [m for m in all_models if not m.__table__.foreign_keys]
            model = random.choice(all_models)
            obj = self.mixer.blend(model)
        obj = obj.as_dict()

        return (model, obj)

    def create_random_item(self, model: models.ProjectModel) -> str:
        """
        Generate a fake database item and insert it into the database.
        """

        _, obj = self.get_random_item(model=model)
        obj_id = db_utils.create_item(model, obj)

        return obj_id
