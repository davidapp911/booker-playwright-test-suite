import os

import pytest
from dotenv import load_dotenv


@pytest.fixture(scope="session")
def base_url():
    load_dotenv()
    return os.getenv("BASE_URL")
