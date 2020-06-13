from starlette.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from starlette.testclient import TestClient

from http_quest import passwords
from http_quest.utils import base64_decode, reverse


def test_require_password(level_path: str, client: TestClient) -> None:
    response = client.get(level_path)

    assert response.status_code == HTTP_403_FORBIDDEN
    assert response.text == "X-Password header is required"


def test_wrong_password(level_path: str, client: TestClient) -> None:
    response = client.get(level_path, headers={"X-Password": "qwerty"})

    assert response.status_code == HTTP_403_FORBIDDEN
    assert response.text == "X-Password header is wrong"


def test_level_1(client: TestClient) -> None:
    response = client.get("/level-1", headers={"X-Password": passwords.LEVEL_1})

    assert response.status_code == HTTP_200_OK
    assert response.json() == {"password": passwords.LEVEL_2}


def test_level_2(client: TestClient) -> None:
    response = client.get("/level-2", headers={"X-Password": passwords.LEVEL_2})

    assert response.status_code == HTTP_200_OK
    assert response.json() == {reverse("password"): reverse(passwords.LEVEL_3)}


def test_level_3(client: TestClient) -> None:
    response = client.get("/level-3", headers={"X-Password": passwords.LEVEL_3})
    encoded_password = response.json()["password"]
    decoded_password = base64_decode(encoded_password)

    assert response.status_code == HTTP_200_OK
    assert decoded_password == passwords.LEVEL_4


def test_level_4(client: TestClient) -> None:
    response = client.get("/level-4", headers={"X-Password": passwords.LEVEL_4})

    assert response.status_code == HTTP_200_OK
    assert response.json() == {"password": "qwerty"}
    assert response.headers["X-Real-Password"] == passwords.LEVEL_5
