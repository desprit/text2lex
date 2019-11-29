"""
Database queries and useful commands.
"""
import inspect
import argparse
from typing import Union, Dict, Any

from redis import StrictRedis, Redis
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import Session

from shared.database import models
from shared.config import (
    POSTGRES_USER,
    POSTGRES_PASS,
    POSTGRES_HOST,
    POSTGRES_NAME,
    POSTGRES_PORT,
    POSTGRES_NAME_TEST,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_PASS,
)


def get_redis_conn(db: int = 0) -> StrictRedis:
    """
    Return Redis connection.
    """

    try:
        from app import app

        if app.config.get("TESTING"):
            db = 1
    except ModuleNotFoundError:
        pass

    redis_conn = Redis(
        REDIS_HOST, REDIS_PORT, password=REDIS_PASS, db=db, decode_responses=True
    )

    return redis_conn


def get_postgres_conn(
    user: str = POSTGRES_USER,
    password: str = POSTGRES_PASS,
    host: str = POSTGRES_HOST,
    port: Union[str, int] = POSTGRES_PORT,
    name: str = POSTGRES_NAME,
) -> Engine:
    """
    Return PostgreSQL engine.
    """

    try:
        from app import app

        if app.config.get("TESTING"):
            name = POSTGRES_NAME_TEST
    except ModuleNotFoundError:
        pass

    return create_engine(
        f"postgresql://{user}:{password}@{host}:{port}/{name}", client_encoding="utf8"
    )


def get_postgres_session(conn: Engine = None) -> Session:
    """
    Return CockroachDB SQLAlchemy session.
    """

    conn = get_postgres_conn() if not conn else conn
    session = sessionmaker(bind=conn)()

    return session


def init_db(name: str = POSTGRES_NAME, conn=None) -> None:
    """
    Create tables listed in models.py.
    """

    conn = get_postgres_conn(name=name) if not conn else conn
    models.Base.metadata.create_all(conn)


def drop_db(name: str = POSTGRES_NAME, conn=None) -> None:
    """
    Drop all tables defined in models.py.
    """

    conn = get_postgres_conn(name=name) if not conn else conn
    models.Base.metadata.drop_all(conn)


def truncate_db(name: str = POSTGRES_NAME):
    """
    Remove data from tables.
    """

    conn = get_postgres_conn(name=name)
    meta = MetaData(bind=conn, reflect=True)
    cursor = conn.connect()
    transaction = cursor.begin()
    for table in meta.sorted_tables:
        cursor.execute(table.delete())
    transaction.commit()


def create_item(model, item: Dict[str, Any], session=None) -> str:
    """
    Create item in the database, return id of created item.
    """

    session_is_empty = not session
    session = session if session else get_postgres_session()
    item_model = model(**item)
    session.add(item_model)
    session.flush()
    item_id = item_model.id
    session.commit()
    if session_is_empty:
        session.close()

    return item_id


def get_items(
    model: models.ProjectModel,
    filters: Dict[str, Any] = None,
    as_dict: bool = False,
    session=None,
):
    """
    Return all items from the database of the given model.
    """

    filters = {} if not filters else filters
    session_is_empty = not session
    session = session if session else get_postgres_session()
    query = session.query(model)
    for filter_name, filter_value in filters.items():
        query = query.filter(getattr(model, filter_name) == filter_value)
    results = query.all()
    if as_dict:
        results = [r.as_dict() for r in results]
    if session_is_empty:
        session.close()

    return results


def get_item(
    model: models.ProjectModel,
    filters: Dict[str, Any] = None,
    as_dict: bool = False,
    session=None,
):
    """
    Return item from database if exists.
    """

    filters = {} if not filters else filters
    session_is_empty = not session
    session = session if session else get_postgres_session()
    query = session.query(model)
    for filter_name, filter_value in filters.items():
        query = query.filter(getattr(model, filter_name) == filter_value)
    result = query.first()
    if result and as_dict:
        result = result.as_dict()
    if session_is_empty:
        session.close()

    return result


def update_item(
    model: models.ProjectModel, item_id: str, item: Dict[str, Any], session=None
):
    """
    Update existing item in the database.
    """

    session_is_empty = not session
    session = session if session else get_postgres_session()
    session.query(model).filter(getattr(model, "id") == item_id).update(item)
    session.commit()
    if session_is_empty:
        session.close()


def delete_item(model: models.ProjectModel, item_id: str, session=None):
    """
    Delete existing item from the database.
    """

    session_is_empty = not session
    session = session if session else get_postgres_session()
    session.query(model).filter(getattr(model, "id") == item_id).delete()
    session.commit()
    if session_is_empty:
        session.close()


def get_models() -> models.ProjectModels:
    """
    Return all database models.
    """

    surebet_models = inspect.getmembers(models, inspect.isclass)
    surebet_models = [m[1] for m in surebet_models if hasattr(m[1], "__tablename__")]

    return surebet_models


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--task", help="Task name.")
    parser.add_argument("-n", "--name", help="Database table name.")
    arguments = vars(parser.parse_args())
    arguments = {k: arguments[k] for k in arguments if arguments[k]}
    task = arguments.pop("task")
    locals()[task](**arguments)
