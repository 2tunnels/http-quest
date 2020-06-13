from starlette.status import (
    HTTP_200_OK,
    HTTP_403_FORBIDDEN,
    HTTP_405_METHOD_NOT_ALLOWED,
)
from starlette.testclient import TestClient

from http_quest import passwords
from http_quest.utils import base64_decode, reverse


def test_require_password(level: dict, client: TestClient) -> None:
    response = client.request(level["method"], level["path"])

    assert response.status_code == HTTP_403_FORBIDDEN
    assert response.text == "X-Password header is required"


def test_wrong_password(level: dict, client: TestClient) -> None:
    response = client.request(
        level["method"], level["path"], headers={"X-Password": "qwerty"}
    )

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


def test_level_5_get_method_not_allowed(client: TestClient) -> None:
    response = client.get("/level-5", headers={"X-Password": passwords.LEVEL_5})

    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED
    assert response.text == "Method Not Allowed"


def test_level_5(client: TestClient) -> None:
    response = client.delete("/level-5", headers={"X-Password": passwords.LEVEL_5})

    assert response.status_code == HTTP_200_OK
    assert response.json() == {"password": passwords.LEVEL_6}
