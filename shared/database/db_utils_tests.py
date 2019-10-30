"""
Tests for db_utils.py
"""
from redis import StrictRedis

from shared.utils.utils import is_equal
from shared.database import models, db_utils
from shared.tests.base import TestsBaseClass
from shared.config import POSTGRES_NAME_TEST


class DbUtilsTests(TestsBaseClass):
    """
    Tests for db_utils.py
    """

    def test_01_get_postgres_conn_testing(self):
        """
        Should return connection to the test database.
        """

        conn = db_utils.get_postgres_conn()
        self.assertEqual(conn.url.database, POSTGRES_NAME_TEST)

    def test_02_init_db(self):
        """
        Should create database.
        """

        for table in models.TABLES:
            self.conn.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
        results = self.conn.execute("SELECT * from pg_catalog.pg_tables").fetchall()
        tables = [t[1] for t in results]
        db_utils.init_db()
        results = self.conn.execute("SELECT * from pg_catalog.pg_tables").fetchall()
        tables = [t[1] for t in results]
        missing_tables = [t for t in models.TABLES if t not in tables]
        self.assertFalse(missing_tables)

    def test_03_drop_db(self):
        """
        Should create database.
        """

        db_utils.init_db()
        db_utils.drop_db()
        results = self.conn.execute("SELECT * from pg_catalog.pg_tables").fetchall()
        tables = [t[1] for t in results]
        existing_tables = [t for t in models.TABLES if t in tables]
        self.assertFalse(any(existing_tables))
        db_utils.init_db()

    def get_create_item(self, session=None):
        """
        Should insert given item in the database.
        """

        model, item = self.get_random_item()
        item_id = db_utils.create_item(model, item, session=session)
        database_item = db_utils.get_item(
            model, filters={"id": item["id"]}, session=session
        )
        self.assertTrue(database_item)
        self.assertEqual(item["id"], item_id)
        database_item = database_item.as_dict()
        items_equal = is_equal(item, database_item)
        self.assertTrue(items_equal)

    def test_04_get_create_item_with_session(self):
        """
        Should insert given item in the database.
        """

        self.get_create_item(session=self.session)

    def test_05_get_create_item_no_session(self):
        """
        Should insert given item in the database.
        """

        self.get_create_item()

    def test_06_create_item_without_session(self):
        """
        Should insert given item in the database.
        """

        model, item = self.get_random_item()
        db_utils.create_item(model, item)
        database_item = db_utils.get_item(model, filters={"id": item["id"]})
        self.assertTrue(database_item)
        database_item = database_item.as_dict()
        items_equal = is_equal(item, database_item)
        self.assertTrue(items_equal)

    def get_items(self, session=None):
        """
        Should return items of the given model as objects.
        """

        model, _ = self.get_random_item()
        for _ in range(3):
            _, item = self.get_random_item(model)
            db_utils.create_item(model, item, session=self.session)
        database_items = db_utils.get_items(model, session=session)
        self.assertTrue(len(database_items) == 3)
        self.assertTrue(all([isinstance(item, model) for item in database_items]))

    def test_07_get_items_as_objects_with_session(self):
        """
        Should return items of the given model as objects.
        """

        self.get_items(session=self.session)

    def test_08_get_items_as_objects_no_session(self):
        """
        Should return items of the given model as objects.
        """

        self.get_items()

    def test_09_get_items_as_dict(self):
        """
        Should return items of the given model as objects.
        """

        for _ in range(3):
            model, item = self.get_random_item()
            db_utils.create_item(model, item, session=self.session)
        database_items = db_utils.get_items(model, as_dict=True, session=self.session)
        self.assertTrue(all([isinstance(item, dict) for item in database_items]))

    def update_item(self, session=None):
        """
        Update item in the database
        """

        model, item = self.get_random_item()
        item_id = db_utils.create_item(model, item, session=session)
        new_id = f"{item_id}-01"
        db_utils.update_item(model, item_id, {"id": new_id}, session=session)
        database_updated_item = db_utils.get_item(
            model, filters={"id": new_id}, session=session
        )
        self.assertTrue(database_updated_item)

    def test_10_update_item_with_session(self, *args, **kwargs):
        """
        Should update given item in the database.
        """

        self.update_item(session=self.session)

    def test_11_update_item_no_session(self, *args, **kwargs):
        """
        Should update given item in the database.
        """

        self.update_item()

    def test_12_get_models(self):
        """
        Should return a list of models.
        """

        project_models = db_utils.get_models()
        self.assertTrue(isinstance(project_models, list))
        self.assertTrue(len(project_models) > 0)

    def delete_item(self, session=None):
        """
        Should delete item from the database with given ID.
        """

        model, item = self.get_random_item()
        db_utils.create_item(model, item)
        db_utils.delete_item(model, item["id"], session=session)
        existing_item = db_utils.get_item(model, filters={"id": item["id"]})
        self.assertFalse(existing_item)

    def test_13_delete_item_with_session(self):
        """
        Should delete item from the database with given ID.
        """

        self.delete_item(session=self.session)

    def test_14_delete_item_no_session(self):
        """
        Should delete item from the database with given ID.
        """

        self.delete_item()

    def test_15_get_redis_conn(self):
        """
        Should return Redis connection object.
        """

        redis_conn = db_utils.get_redis_conn()
        self.assertIsInstance(redis_conn, StrictRedis)
