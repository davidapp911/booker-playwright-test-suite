import pytest
from playwright.sync_api import Page, expect

from helpers import apply_field_rules, fake_contact
from pages.contact_page import ContactPage
from tests.ui.data.contact_page_cases import MISSING_FIELD


@pytest.mark.contact
def test_valid_contact_form(page: Page, base_url, delete_message):
    contact_data = fake_contact()
    delete_message(contact_data["name"])
    page_obj = ContactPage(page)
    page_obj.load_contact_page(base_url)
    page_obj.fill_contact_form(**contact_data)
    page_obj.submit_contact_form()
    expect(page_obj.success_message()).to_be_visible()


@pytest.mark.contact
@pytest.mark.parametrize("case", MISSING_FIELD)
def test_missing_required_field(page: Page, base_url, case):
    contact_data = apply_field_rules(fake_contact(), missing=case["missing_field"])
    page_obj = ContactPage(page)
    page_obj.load_contact_page(base_url)
    page_obj.fill_contact_form(**contact_data)
    page_obj.submit_contact_form()
    expect(page_obj.missing_field_alert(case["expected_error"])).to_be_visible()


@pytest.mark.contact
def test_admin_received_message(page: Page, base_url, delete_message, auth_client):
    contact_data = fake_contact()
    delete_message(contact_data["name"])
    page_obj = ContactPage(page)
    page_obj.load_contact_page(base_url)
    page_obj.fill_contact_form(**contact_data)
    page_obj.submit_contact_form()

    response = auth_client.get("/api/message")
    messages = response.json()["messages"]
    message_id = next((message["id"] for message in messages if message["name"] == contact_data["name"]), None)

    assert message_id
