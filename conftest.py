import os

import pytest
from dotenv import load_dotenv
from faker import Faker


@pytest.fixture(scope="session")
def base_url():
    load_dotenv()
    return os.getenv("BASE_URL")


@pytest.fixture()
def person_generator():
    faker = Faker()
    return {
        "first_name": length_select(faker.first_name, 3, 21),
        "last_name": length_select(faker.last_name, 3, 21),
        "email": faker.email(),
        "phone": faker.numerify("###########"),
    }


def length_select(func, min, max):
    name = func()
    while not (min <= len(name) <= max):
        name = func()

    return name
