from typing import Generator

import pytest
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from app.db.base_class import Base
from app.db.test_session import TestingSessionLocal
from app.db.test_session import test_engine
from app.dependencies.auth_db import get_db
from app.main import app


@pytest.fixture(scope="session", autouse=True)
def set_test_db() -> None:
    """Reset database after each test session"""
    Base.metadata.drop_all(bind=test_engine)  # pylint: disable=no-member
    Base.metadata.create_all(bind=test_engine)  # pylint: disable=no-member


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    """Create a clean database session for a test."""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    nested = connection.begin_nested()

    @sqlalchemy.event.listens_for(session, "after_transaction_end")
    def end_savepoint(session, transaction):  # pylint: disable=unused-argument
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(db_session: sessionmaker) -> Generator[TestClient, None, None]:  # pylint: disable=redefined-outer-name
    """Create a test client for the app."""

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]
