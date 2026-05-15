from datetime import date, timedelta

from faker import Faker


def fake_booking():
    fake = Faker()
    return {
        "roomid": 1,
        "firstname": bounded(fake.first_name, 3, 21),
        "lastname": bounded(fake.last_name, 3, 21),
        "depositpaid": "true",
        "email": fake.email(),
        "phone": fake.numerify("###############"),
        "bookingdates": {"checkin": relative_date(), "checkout": relative_date(5)},
    }


def fake_room() -> dict:
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


def fake_contact() -> dict:
    fake = Faker()

    return {
        "name": bounded(fake.name, 10, 30),
        "email": fake.email(),
        "phone": fake.numerify("###############"),
        "subject": "Inquiry about a room",
        "description": "Hey is room 123 available. It's my lucky number",
    }


def bounded(func, min: int, max: int):
    while True:
        func_output = func()
        if min <= len(func_output) <= max:
            return func_output


def relative_date(offset: int = 0):
    return str(date.today() + timedelta(days=offset))


def apply_field_rules(
    data: dict, exclude: list[str] = [], missing: list[str] = []
) -> dict:
    return {k: ("" if k in missing else v) for k, v in data.items() if k not in exclude}
