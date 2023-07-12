from starlette import status
from starlette.testclient import TestClient


def test_health(client: TestClient):
    """Test health endpoint."""
    response = client.get("api/v1/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "It works ✨!"}
