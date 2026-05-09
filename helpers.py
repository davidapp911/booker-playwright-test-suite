from datetime import date, timedelta

from faker import Faker


def person_generator():
    faker = Faker()
    return {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "email": faker.email(),
        "phone": faker.numerify("###########"),
    }


def force_length(func, min: int, max: int):
    while True:
        func_output = func()
        if min <= len(func_output) <= max:
            return func_output


def date_generator_from_today(offset: int = 0):
    return str(date.today() + timedelta(days=offset))
