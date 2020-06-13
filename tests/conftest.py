import pytest
from _pytest.fixtures import SubRequest
from starlette.applications import Starlette
from starlette.testclient import TestClient

from http_quest.asgi import application


@pytest.fixture(params=["/level-1", "/level-2", "/level-3", "/level-4"])
def level_path(request: SubRequest) -> str:
    param: str = request.param

    return param


@pytest.fixture
def app() -> Starlette:
    return application


@pytest.fixture
def client(app: Starlette) -> TestClient:
    return TestClient(application)
