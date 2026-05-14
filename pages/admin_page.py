from playwright.sync_api import expect

from pages.base_page import BasePage


class AdminPage(BasePage):
    def load_admin_page(self, base_url: str):
        self.navigate(f"{base_url}/admin")

    def fill_login_form(self, username: str, password: str):
        self.page.get_by_role("textbox", name="Username").fill(username)
        self.page.get_by_role("textbox", name="Password").fill(password)

    def submit_login(self):
        self.page.get_by_role("button", name="Login").click()
        self.page.wait_for_url("**/admin**")

    def login(self, username, password):
        self.fill_login_form(username, password)
        self.submit_login()

    def room_form(self):
        return self.page.get_by_test_id("roomName")

    def invalid_login_alert(self):
        return self.page.get_by_text("Invalid credentials")

    def fill_room_form(
        self,
        roomName: str,
        type: str,
        accessible: str,
        roomPrice: int,
        features: list[str],
    ):
        self.page.get_by_test_id("roomName").fill(roomName)
        self.page.locator("#type").select_option(type)
        self.page.locator("#accessible").select_option(accessible)
        self.page.locator("#roomPrice").fill(str(roomPrice))

        for feature in features:
            self.page.get_by_role("checkbox", name=feature).check()

    def submit_new_room(self):
        self.page.get_by_role("button", name="Create").click()

    def new_room_created(self, room_number: str):
        return self.page.get_by_text(room_number)

    def open_room_page(self, room_name: str):
        self.page.locator('[data-testid="roomlisting"]').filter(has=self.page.locator(f"#roomName{room_name}")).click()

    def click_edit_button(self):
        self.page.get_by_role("button", name="Edit").click()

    def change_room_price(self, new_price: str):
        expect(self.page.get_by_role("textbox", name="Room price:")).not_to_be_empty()
        self.page.get_by_role("textbox", name="Room price:").fill(new_price)

    def click_update_button(self):
        self.page.get_by_role("button", name="Update").click()

    def room_price(self):
        return self.page.get_by_text("Room price:")

    def delete_room(self, room_number):
        self.page.locator('[data-testid="roomlisting"]').filter(has_text=room_number).locator("span.roomDelete").click()

    def room_to_delete(self, room_number):
        return self.page.locator(f"#roomName{room_number}")
