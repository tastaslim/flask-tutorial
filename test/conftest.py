import pytest
from app import create_app
from config import DB_URL


@pytest.fixture()
def app():
    app = create_app(DB_URL)
    app.config.update(
        {
            "TESTING": True,
        }
    )

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
