import pytest
from _pytest.fixtures import SubRequest
from starlette.applications import Starlette
from starlette.testclient import TestClient

from http_quest.asgi import application


@pytest.fixture(
    params=[
        {"path": "/level-1", "method": "GET"},
        {"path": "/level-2", "method": "GET"},
        {"path": "/level-3", "method": "GET"},
        {"path": "/level-4", "method": "GET"},
        {"path": "/level-5", "method": "DELETE"},
        {"path": "/level-6", "method": "GET"},
        {"path": "/level-7", "method": "GET"},
    ]
)
def level(request: SubRequest) -> dict:
    param: dict = request.param

    return param


@pytest.fixture
def app() -> Starlette:
    return application


@pytest.fixture
def client(app: Starlette) -> TestClient:
    return TestClient(application)
