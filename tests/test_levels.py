import pytest
from starlette import status
from starlette.applications import Starlette
from starlette.testclient import TestClient

from http_quest import passwords, secrets
from http_quest.utils import base64_decode

from .conftest import Level


def test_require_password(level: Level, app: Starlette, client: TestClient) -> None:
    url = app.url_path_for(level.get_route_name())
    response = client.request(level.method, url)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.text == "X-Password header is required"


def test_wrong_password(level: Level, app: Starlette, client: TestClient) -> None:
    url = app.url_path_for(level.get_route_name())
    response = client.request(level.method, url, headers={"X-Password": "qwerty"})

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.text == "X-Password header is wrong"


def test_plain(client: TestClient, app: Starlette) -> None:
    response = client.get(
        app.url_path_for("level:plain"), headers={"X-Password": passwords.PLAIN}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"password": passwords.REVERSE}


def test_reverse(client: TestClient, app: Starlette) -> None:
    response = client.get(
        app.url_path_for("level:reverse"), headers={"X-Password": passwords.REVERSE}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"drowssap": passwords.BASE64[::-1]}


def test_base64(client: TestClient, app: Starlette) -> None:
    response = client.get(
        app.url_path_for("level:base64"), headers={"X-Password": passwords.BASE64}
    )
    encoded_password = response.json()["password"]
    decoded_password = base64_decode(encoded_password)

    assert response.status_code == status.HTTP_200_OK
    assert decoded_password == passwords.HEADERS


def test_header(client: TestClient, app: Starlette) -> None:
    response = client.get(
        app.url_path_for("level:header"), headers={"X-Password": passwords.HEADERS}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"password": "qwerty"}
    assert response.headers["X-Real-Password"] == passwords.DELETE


@pytest.mark.parametrize("method", ["GET", "POST", "PUT", "PATCH"])
def test_delete_method_not_allowed(
    method: str, client: TestClient, app: Starlette
) -> None:
    response = client.request(
        method,
        app.url_path_for("level:delete"),
        headers={"X-Password": passwords.DELETE},
    )

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert response.text == "Method Not Allowed"


def test_delete(client: TestClient, app: Starlette) -> None:
    response = client.delete(
        app.url_path_for("level:delete"), headers={"X-Password": passwords.DELETE}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"password": passwords.USER_AGENT}


def test_user_agent_is_not_ie_6(client: TestClient, app: Starlette) -> None:
    response = client.get(
        app.url_path_for("level:user_agent"),
        headers={"X-Password": passwords.USER_AGENT},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.text == (
        "Password for the next level is only available for the bravest! "
        "Internet Explorer 6 users!"
    )


def test_user_agent(client: TestClient, app: Starlette) -> None:
    response = client.get(
        app.url_path_for("level:user_agent"),
        headers={
            "X-Password": passwords.USER_AGENT,
            "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)",
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"password": passwords.ACCEPT_LANGUAGE}


def test_accept_language_is_not_provided(client: TestClient, app: Starlette) -> None:
    response = client.get(
        app.url_path_for("level:accept_language"),
        headers={"X-Password": passwords.ACCEPT_LANGUAGE},
    )

    assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE
    assert response.text == "Я говорю только по русски, товарищ."


def test_accept_language_is_not_russian(client: TestClient, app: Starlette) -> None:
    response = client.get(
        app.url_path_for("level:accept_language"),
        headers={
            "X-Password": passwords.ACCEPT_LANGUAGE,
            "Accept-Language": "en-US,en;q=0.5",
        },
    )

    assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE
    assert response.text == "Я говорю только по русски, товарищ."


def test_accept_language(client: TestClient, app: Starlette) -> None:
    response = client.get(
        app.url_path_for("level:accept_language"),
        headers={"X-Password": passwords.ACCEPT_LANGUAGE, "Accept-Language": "ru-RU"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"пароль": passwords.REDIRECT}


def test_redirect_secret_is_wrong(client: TestClient, app: Starlette) -> None:
    response = client.get(
        app.url_path_for("level:redirect") + "?secret=qwerty",
        headers={"X-Password": passwords.REDIRECT},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.text == "Secret is wrong."


def test_redirect(client: TestClient, app: Starlette) -> None:
    response = client.get(
        app.url_path_for("level:redirect"), headers={"X-Password": passwords.REDIRECT}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"password": passwords.ROBOTS}
    assert len(response.history) == 20


def test_robots_secret_is_missing(client: TestClient, app: Starlette) -> None:
    response = client.post(
        app.url_path_for("level:robots"), headers={"X-Password": passwords.ROBOTS}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "errors": {"secret": ["Missing data for required field."]}
    }


def test_robots_secret_is_wrong(client: TestClient, app: Starlette) -> None:
    response = client.post(
        app.url_path_for("level:robots"),
        headers={"X-Password": passwords.ROBOTS},
        json={"secret": "foobar"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.text == "Secret is wrong, human."


def test_robots(client: TestClient, app: Starlette) -> None:
    response = client.post(
        app.url_path_for("level:robots"),
        headers={"X-Password": passwords.ROBOTS},
        json={"secret": secrets.ROBOTS},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"password": passwords.GUESS_NUMBER}


def test_guess_number_is_missing(client: TestClient, app: Starlette) -> None:
    response = client.post(
        app.url_path_for("level:guess_number"),
        headers={"X-Password": passwords.GUESS_NUMBER},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "errors": {"number": ["Missing data for required field."]}
    }


def test_guess_number_is_not_a_valid_integer(
    client: TestClient, app: Starlette
) -> None:
    response = client.post(
        app.url_path_for("level:guess_number"),
        headers={"X-Password": passwords.GUESS_NUMBER},
        json={"number": "foobar"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"errors": {"number": ["Not a valid integer."]}}


@pytest.mark.parametrize("number", [0, 1001])
def test_guess_number_invalid_range(
    number: int, client: TestClient, app: Starlette
) -> None:
    response = client.post(
        app.url_path_for("level:guess_number"),
        headers={"X-Password": passwords.GUESS_NUMBER},
        json={"number": number},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "errors": {
            "number": [
                "Must be greater than or equal to 1 and less than or equal to 1000."
            ]
        }
    }


def test_guess_number_is_wrong(client: TestClient, app: Starlette) -> None:
    response = client.post(
        app.url_path_for("level:guess_number"),
        headers={"X-Password": passwords.GUESS_NUMBER},
        json={"number": 100},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.text == "Number is wrong."


def test_guess_number(client: TestClient, app: Starlette) -> None:
    response = client.post(
        app.url_path_for("level:guess_number"),
        headers={"X-Password": passwords.GUESS_NUMBER},
        json={"number": 372},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"password": passwords.MASK}


def test_mask_secret_is_missing(client: TestClient, app: Starlette) -> None:
    response = client.post(
        app.url_path_for("level:mask"), headers={"X-Password": passwords.MASK}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "errors": {"secret": ["Missing data for required field."]}
    }


def test_mask_secret_is_wrong(client: TestClient, app: Starlette) -> None:
    response = client.post(
        app.url_path_for("level:mask"),
        headers={"X-Password": passwords.MASK},
        json={"secret": "eeeeeeeeeeeeeeeeeeee"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"password": "***u****7***********"}


def test_mask(client: TestClient, app: Starlette) -> None:
    response = client.post(
        app.url_path_for("level:mask"),
        headers={"X-Password": passwords.MASK},
        json={"secret": secrets.MASK},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"password": passwords.FINISH}


def test_finish(client: TestClient, app: Starlette) -> None:
    response = client.get(
        app.url_path_for("level:finish"), headers={"X-Password": passwords.FINISH},
    )

    assert response.status_code == status.HTTP_200_OK
    assert "You have completed the very last level of HTTP quest." in response.text
