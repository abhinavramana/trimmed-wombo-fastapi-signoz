import logging
import os
from contextlib import contextmanager

import testing.postgresql
from sqlalchemy import Table, MetaData
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql.ddl import DropTable

TEST_DB_PATH = "/tmp/my_test_db"


def remove_file_if_exists(filepath: str):
    if os.path.exists(filepath):
        os.remove(filepath)


def drop_table_if_exists(engine: Engine, table_name):
    try:
        drop_table(engine, table_name)
    except:
        print(f"Maybe table {table_name} doesn't exist, so can't drop")


def recreate_table_if_required(engine: Engine, table_name: str, metadata: MetaData, table: Table):
    drop_table_if_exists(engine, table_name)
    metadata.create_all(engine, table)


remove_file_if_exists(TEST_DB_PATH)

# Port will be useful to run multiple tests in parallel
POSTGRESQL_TEST = testing.postgresql.Postgresql(name="testdb", port=5678, path=TEST_DB_PATH)
# Before importing anything else related to wombo, we need to override DATABASE_URL
os.environ["DATABASE_URL"] = POSTGRESQL_TEST.url()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def create_db_session(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)()


def drop_table(engine: Engine, table_name):
    with engine.connect() as conn:
        conn.execute(DropTable(
            Table(table_name, MetaData())
        ))


def create_table(engine: Engine, table_name, *args):
    if not engine.dialect.has_table(engine, table_name):  # If table don't exist, Create.
        metadata = MetaData(engine)
        # Create a table with the appropriate Columns
        Table(table_name, metadata, *args)

        # Implement the creation
        metadata.create_all()


def make_engine(database_url, pool_size, max_overflow):
    engine = create_engine(
        database_url,
        pool_size=pool_size,
        max_overflow=max_overflow,
        echo=True
    )
    return engine


def database_session(engine=None):
    session: Session = create_db_session(engine)
    try:
        yield session
        if session.dirty:
            session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def get_db_session_context(database_url, pool_size, max_overflow):
    engine = make_engine(database_url, pool_size, max_overflow)

    def get_database_session():
        return database_session(engine)

    database_session_context = contextmanager(get_database_session)
    logger.info(f"Main Database session created with : {database_url}")

    return database_session_context, engine


DatabaseSession, DB_ENGINE = get_db_session_context(POSTGRESQL_TEST.url(), 1, 1)
DatabaseRecord = declarative_base()
