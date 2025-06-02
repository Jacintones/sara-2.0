import pytest
from django.contrib.auth import get_user_model
from ninja.testing import TestClient
from apps.authenticate.api.v1.auth_v1_api import router as auth_router

@pytest.fixture
def auth_header(create_test_user):
    client = TestClient(auth_router)
    response = client.post("/login", json={
        "email": "admin@example.com",
        "password": "admin123",
        "remember_me": False
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
