import pytest
from uuid import uuid4
from datetime import datetime
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_user():
    test_user_data = {
        "email": "example@example.com",
        "username": "example_user"
    }
    response = client.post("/users", json=test_user_data)
    print(response.json())  # Для налагодження
    assert response.status_code == 200


def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200


def test_get_user_not_found():
    random_uuid = str(uuid4())
    response = client.get(f"/users/{random_uuid}")
    assert response.status_code == 404


def test_update_user():
    # Додаємо нового юзера перед оновленням
    create_response = client.post("/users", json={
        "email": "boby@example.com",
        "username": "example_user"
    })
    assert create_response.status_code == 200

    user_id = create_response.json()["id"]
    update_response = client.put(f"/users/{user_id}", json={
        "isdisabled": True,
    })
    print(update_response.json())
    assert update_response.status_code == 200


def test_delete_user():
    # Додаємо нового юзера перед видаленням
    create_response = client.post("/users", json={
        "email": "boby2thesequel@example.com",
        "username": "example_user"
    })
    assert create_response.status_code == 200

    user_id = create_response.json()["id"]
    delete_response = client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 200
