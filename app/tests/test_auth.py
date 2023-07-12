from sqlalchemy.orm import Session
from starlette import status
from starlette.testclient import TestClient

from app.models import User


def test_signup(client: TestClient, db_session: Session):
    """Test signup endpoint."""
    response = client.post(
        "/api/v1/auth/signup",
        json={
            "email": "test@example.com",
            "password": "password",
            "username": "test",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"message": "Created user successfully!"}
    assert db_session.query(User).count() == 1


def test_signup_with_empty_payload(client: TestClient, db_session: Session):
    """Test signup endpoint with empty payload."""
    response = client.post("/api/v1/auth/signup", json={})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_signup_with_not_valid_email(client: TestClient, db_session: Session):
    """Test signup endpoint with not valid email."""
    response = client.post(
        "/api/v1/auth/signup",
        json={
            "email": "testexample.com",
            "password": "password",
            "username": "test",
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {
        "detail": [{"loc": ["body", "email"], "msg": "value is not a valid email address", "type": "value_error.email"}]
    }
