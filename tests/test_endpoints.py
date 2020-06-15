from starlette import status
from starlette.applications import Starlette
from starlette.testclient import TestClient

from http_quest import passwords, secrets


def test_home(client: TestClient, app: Starlette) -> None:
    response = client.get(app.url_path_for("home"))

    assert response.status_code == status.HTTP_200_OK
    assert passwords.PLAIN in response.text


def test_robots(client: TestClient, app: Starlette) -> None:
    response = client.get(app.url_path_for("robots"))

    assert response.status_code == status.HTTP_200_OK
    assert secrets.ROBOTS in response.text
