from fastapi.testclient import TestClient
from main import app
import pytest
import random
import string

client = TestClient(app)

@pytest.fixture
def auth_headers():
    # random_username = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    # Register a test user
    client.post("/users/", json={"username": "testuser", "password": "testpassword"})

    # Authenticate and get token
    response = client.post("/token", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    token = response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    return headers


def test_read_books(auth_headers):
    response = client.get("/books/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_book(auth_headers):
    book_data = {
        "title": "Test Book",
        "author_id": 1,
        "genre_id": 1,
        "publication_date": "2021-01-01",
        "price": 29.99
    }
    response = client.post("/books/", json=book_data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Book"
