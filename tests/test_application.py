from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_406_NOT_ACCEPTABLE,
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


def test_level_6_wrong_secret(client: TestClient) -> None:
    response = client.get(
        "/level-6?secret=qwerty", headers={"X-Password": passwords.LEVEL_6}
    )

    assert response.status_code == HTTP_403_FORBIDDEN
    assert response.text == "Wrong secret"


def test_level_6(client: TestClient) -> None:
    response = client.get("/level-6", headers={"X-Password": passwords.LEVEL_6})

    assert response.status_code == HTTP_200_OK
    assert len(response.history) == 20


def test_level_7_non_ie_6(client: TestClient) -> None:
    response = client.get("/level-7", headers={"X-Password": passwords.LEVEL_7})

    assert response.status_code == HTTP_403_FORBIDDEN
    assert response.text == (
        "Password for the next level is only available for the bravest! "
        "Internet Explorer 6 users!"
    )


def test_level_7(client: TestClient) -> None:
    response = client.get(
        "/level-7",
        headers={
            "X-Password": passwords.LEVEL_7,
            "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)",
        },
    )

    assert response.status_code == HTTP_200_OK
    assert response.json() == {"password": passwords.LEVEL_8}


def test_level_8_number_is_missing(client: TestClient) -> None:
    response = client.post("/level-8", headers={"X-Password": passwords.LEVEL_8})

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json() == {
        "errors": {"number": ["Missing data for required field."]}
    }


def test_level_8_number_is_not_a_valid_integer(client: TestClient) -> None:
    response = client.post(
        "/level-8", headers={"X-Password": passwords.LEVEL_8}, json={"number": "foobar"}
    )

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json() == {"errors": {"number": ["Not a valid integer."]}}


def test_level_8_number_invalid_range(client: TestClient) -> None:
    response = client.post(
        "/level-8", headers={"X-Password": passwords.LEVEL_8}, json={"number": 0}
    )

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json() == {
        "errors": {
            "number": [
                "Must be greater than or equal to 1 and less than or equal to 1000."
            ]
        }
    }


def test_level_8_wrong_number(client: TestClient) -> None:
    response = client.get(
        "/level-8?number=100", headers={"X-Password": passwords.LEVEL_8}
    )

    assert response.status_code == HTTP_403_FORBIDDEN
    assert response.text == "Wrong number."


def test_level_8(client: TestClient) -> None:
    response = client.get(
        "/level-8?number=372", headers={"X-Password": passwords.LEVEL_8}
    )

    assert response.status_code == HTTP_200_OK
    assert response.json() == {"password": passwords.LEVEL_9}


def test_level_9_accept_language_is_not_provided(client: TestClient) -> None:
    response = client.get("/level-9", headers={"X-Password": passwords.LEVEL_9})

    assert response.status_code == HTTP_406_NOT_ACCEPTABLE
    assert response.text == "Я говорю только по русски, товарищ."


def test_level_9_non_russian_accept_language(client: TestClient) -> None:
    response = client.get(
        "/level-9",
        headers={"X-Password": passwords.LEVEL_9, "Accept-Language": "en-US,en;q=0.5"},
    )

    assert response.status_code == HTTP_406_NOT_ACCEPTABLE
    assert response.text == "Я говорю только по русски, товарищ."


def test_level_9(client: TestClient) -> None:
    response = client.get(
        "/level-9",
        headers={"X-Password": passwords.LEVEL_9, "Accept-Language": "ru-RU"},
    )

    assert response.status_code == HTTP_200_OK
    assert response.json() == {"пароль": passwords.LEVEL_10}


def test_level_10_entry(client: TestClient) -> None:
    response = client.get("/level-10", headers={"X-Password": passwords.LEVEL_10})

    assert response.status_code == HTTP_200_OK
    assert response.json() == {"url": "http://testserver/level-10/{secret}"}


def test_level_10_secret_wrong_secret(client: TestClient) -> None:
    response = client.get(
        "/level-10/eeeeeeeeeeeeeeeeeeee", headers={"X-Password": passwords.LEVEL_10}
    )

    assert response.status_code == HTTP_200_OK
    assert response.json() == {"password": "***L****9***********"}


def test_level_10_secret(client: TestClient) -> None:
    response = client.get(
        "/level-10/6fjeXUuve5Wm2nR6gsbQ", headers={"X-Password": passwords.LEVEL_10}
    )

    assert response.status_code == HTTP_200_OK
    assert response.json() == {"password": passwords.LEVEL_11}
