from starlette.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from starlette.testclient import TestClient

from http_quest import passwords
from http_quest.main import application


def test_level_1_require_password():
    client = TestClient(application)
    response = client.get("/level-1")

    assert response.status_code == HTTP_403_FORBIDDEN
    assert response.text == "X-Password header is required"


def test_level_1_wrong_password():
    client = TestClient(application)
    response = client.get("/level-1", headers={"X-Password": "qwerty"})

    assert response.status_code == HTTP_403_FORBIDDEN
    assert response.text == "X-Password header is wrong"


def test_level_1_correct_password():
    client = TestClient(application)
    response = client.get("/level-1", headers={"X-Password": passwords.LEVEL_1})

    assert response.status_code == HTTP_200_OK
    assert response.json() == {"password": passwords.LEVEL_2}
