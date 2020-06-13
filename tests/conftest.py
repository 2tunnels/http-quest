import pytest
from starlette.applications import Starlette
from starlette.testclient import TestClient

from http_quest.asgi import application


@pytest.fixture
def app() -> Starlette:
    return application


@pytest.fixture
def client(app: Starlette) -> TestClient:
    return TestClient(application)
