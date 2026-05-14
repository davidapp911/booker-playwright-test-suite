import pytest

from api.client import BookerClient


@pytest.fixture(scope="session")
def client(base_url):
    return BookerClient(base_url)
