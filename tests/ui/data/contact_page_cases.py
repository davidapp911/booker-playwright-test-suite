from faker import Faker

faker = Faker()

MISSING_FIELD = [
    {
        "missing_field": ["name"],
        "expected_error": "Name may not be blank",
    },
    {
        "missing_field": ["email"],
        "expected_error": "Email may not be blank",
    },
    {
        "missing_field": ["phone"],
        "expected_error": "Phone may not be blank",
    },
    {
        "missing_field": ["subject"],
        "expected_error": "Subject may not be blank",
    },
    {
        "missing_field": ["description"],
        "expected_error": "Message may not be blank",
    },
]
