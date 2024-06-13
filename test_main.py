from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_read_books():
    response = client.get("/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_book():
    response = client.post("/books/", json={
        "title": "Test Book",
        "author_id": 1,
        "genre_id": 1,
        "publication_date": "2021-01-01",
        "price": 29.99
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Test Book"
