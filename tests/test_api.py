from fastapi.testclient import TestClient
from app import app
import pytest
from config.db import conn

############################EXTRA FUNCTIONS##################################


def get_random_existing_document_ids(num_ids):
    existing_document_ids = [
        str(doc["_id"])
        for doc in conn.local.user.aggregate([{"$sample": {"size": num_ids}}])
    ]
    return existing_document_ids


############################TEST FUNCTIONS##################################


@pytest.fixture()
def client():
    return TestClient(app)


def test_get_users(client: TestClient):
    response = client.get(
        "/users",
    )
    assert response.status_code == 200


def test_create_user(client: TestClient):
    payload = {
        "name": "test",
        "email": "thisisatest@gmail.com",
        "password": "test_password",
    }
    response = client.post("/users", json=payload)
    assert response.status_code == 201


@pytest.mark.parametrize("id", get_random_existing_document_ids(1))
def test_find_user(client: TestClient, id: str):
    response = client.get(
        f"/users/{id}",
    )
    assert response.status_code == 200


def test_update_user(client: TestClient):
    id = "6501c6dfd285ed2eb16e9fbd"
    payload = {
        "name": "test_updated",
        "email": "test_updated@gmail.com",
        "password": "test_password_updated",
    }
    try:
        response = client.put(f"/users/{id}", json=payload)
        assert (
            response.status_code == 200
        ), f"Expected status code 200, but got {response.status_code}"
    except Exception as e:
        assert False, f"An exception occurred: {str(e)}"
