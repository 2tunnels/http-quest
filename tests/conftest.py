from dataclasses import dataclass

import pytest
from _pytest.fixtures import SubRequest
from starlette.applications import Starlette
from starlette.testclient import TestClient

from http_quest.asgi import application


@dataclass
class Level:
    name: str
    method: str

    def get_route_name(self) -> str:
        return f"level:{self.name}"


def get_level_name(level: Level) -> str:
    return level.name


@pytest.fixture(
    params=[
        Level("plain", "GET"),
        Level("reverse", "GET"),
        Level("base64", "GET"),
        Level("header", "GET"),
        Level("delete", "DELETE"),
        Level("user_agent", "GET"),
        Level("accept_language", "GET"),
        Level("redirect", "GET"),
        Level("robots", "POST"),
        Level("guess_number", "POST"),
        Level("mask", "POST"),
        Level("finish", "GET"),
    ],
    ids=get_level_name,
)
def level(request: SubRequest) -> Level:
    param: Level = request.param

    return param


@pytest.fixture
def app() -> Starlette:
    return application


@pytest.fixture
def client(app: Starlette) -> TestClient:
    return TestClient(application)
