from pages.base_page import BasePage


class BookingPage(BasePage):
    def load_room_booking(self, base_url: str, room_id: int, checkin: str, checkout: str):
        url = f"{base_url}/reservation/{room_id}?checkin={checkin}&checkout={checkout}"
        self.navigate(url)

    def click_reserve_now(self):
        self.page.get_by_role("button", name="Reserve Now").click()

    def fill_reservation_form(self, firstname: str, lastname: str, email: str, phone: str):
        self.page.get_by_role("textbox", name="Firstname").fill(firstname)
        self.page.get_by_role("textbox", name="Lastname").fill(lastname)
        self.page.get_by_role("textbox", name="Email").fill(email)
        self.page.get_by_role("textbox", name="Phone").fill(phone)

    def confirmation(self):
        return self.page.get_by_role("heading", name="Booking Confirmed")

    def empty_field_alert(self):
        return self.page.get_by_role("alert").filter(has_text="Lastname should not be")

    def load_error(self):
        return self.page.get_by_role("heading", name="This page couldn’t load")
