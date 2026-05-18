from collections.abc import Callable
from datetime import date, timedelta
from typing import Any

from faker import Faker


def fake_booking() -> dict[str, Any]:
    fake = Faker()
    return {
        "roomid": fake.random_int(min=1, max=3),
        "firstname": bounded(fake.first_name, 3, 21),
        "lastname": bounded(fake.last_name, 3, 21),
        "depositpaid": str(fake.boolean()).lower(),
        "email": fake.email(),
        "phone": fake.numerify("###############"),
        "bookingdates": fake_booking_dates(),
    }


def fake_booking_dates() -> dict[str, Any]:
    fake = Faker()
    random_offset = fake.random_int(min=365, max=1000)
    random_booking_lenght = fake.random_int(min=1, max=5)
    return {
        "checkin": relative_date(random_offset),
        "checkout": relative_date(random_offset + random_booking_lenght),
    }


def fake_room() -> dict[str, Any]:
    fake = Faker()
    room_type = ["Single", "Twin", "Double", "Family", "Suite"]
    features = ["WiFi", "TV", "Radio", "Refreshments", "Safe", "Views"]
    return {
        "roomName": fake.numerify("###"),
        "type": fake.random_element(room_type),
        "accessible": str(fake.boolean()).lower(),
        "image": "https://blog.postman.com/wp-content/uploads/2014/07/logo.png",
        "description": "This is a test room. Stay out of here",
        "roomPrice": fake_price(),
        "features": fake.random_elements(features, unique=True),
    }


def fake_price() -> int:
    return Faker().random_int(min=1, max=999)


def fake_contact() -> dict[str, Any]:
    fake = Faker()

    return {
        "name": bounded(fake.name, 10, 30),
        "email": fake.email(),
        "phone": fake.numerify("###############"),
        "subject": "Inquiry about a room",
        "description": "Hey is room 123 available. It's my lucky number",
    }


def bounded(func: Callable[[], str], min: int, max: int) -> str:
    while True:
        func_output = func()
        if min <= len(func_output) <= max:
            return func_output


def relative_date(offset: int = 0) -> str:
    return str(date.today() + timedelta(days=offset))


def apply_field_rules(data: dict[str, Any], exclude: list[str] = [], missing: list[str] = []) -> dict[str, Any]:
    return {k: ("" if k in missing else v) for k, v in data.items() if k not in exclude}
