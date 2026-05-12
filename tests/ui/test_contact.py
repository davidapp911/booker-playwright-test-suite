import pytest
from playwright.sync_api import Page

from helpers import apply_field_rules, fake_contact
from pages.contact_page import ContactPage
from tests.ui.data.contact_page_cases import MISSING_FIELD


@pytest.mark.contact
def test_valid_contact_form(page: Page, base_url):
    contact_data = fake_contact()
    page_obj = ContactPage(page)
    page_obj.load_contact_page(base_url)
    page_obj.fill_contact_form(**contact_data)
    page_obj.submit_contact_form()
    page_obj.success_message_is_visible()


@pytest.mark.contact
@pytest.mark.parametrize("case", MISSING_FIELD)
def test_missing_required_field(page: Page, base_url, case):
    contact_data = apply_field_rules(fake_contact(), missing=case["missing_field"])
    page_obj = ContactPage(page)
    page_obj.load_contact_page(base_url)
    page_obj.fill_contact_form(**contact_data)
    page_obj.submit_contact_form()
    page_obj.missing_field_alert_is_visible(case["expected_error"])
