import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core import settings

test_engine = create_engine(settings.TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@sqlalchemy.event.listens_for(test_engine, "connect")
def do_connect(dbapi_connection, connection_record):
    dbapi_connection.isolation_level = None


@sqlalchemy.event.listens_for(test_engine, "begin")
def do_begin(conn):
    conn.exec_driver_sql("BEGIN")
