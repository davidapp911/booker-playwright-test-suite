from playwright.sync_api import expect

from pages.base_page import BasePage


class ContactPage(BasePage):
    def load_contact_page(self, base_url):
        self.navigate(f"{base_url}#contact")

    def fill_contact_form(
        self, name: str, email: str, phone: str, subject: str, description: str
    ):
        self.page.get_by_test_id("ContactName").fill(name)
        self.page.get_by_test_id("ContactEmail").fill(email)
        self.page.get_by_test_id("ContactPhone").fill(phone)
        self.page.get_by_test_id("ContactSubject").fill(subject)
        self.page.get_by_test_id("ContactDescription").fill(description)

    def submit_contact_form(self):
        self.page.get_by_role("button", name="Submit").click()

    def success_message_is_visible(self):
        expect(
            self.page.get_by_role("heading", name="Thanks for getting in touch")
        ).to_be_visible()

    def missing_field_alert_is_visible(self, expected_alert):
        expect(self.page.get_by_text(expected_alert)).to_be_visible()
