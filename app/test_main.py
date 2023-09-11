from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_redirect():
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert b"<!DOCTYPE html>" in response.content

def test_staticapp():
    response = client.get("/staticapp")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert b"<!DOCTYPE html>" in response.content
