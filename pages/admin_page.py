from playwright.sync_api import Locator, expect

from pages.base_page import BasePage


class AdminPage(BasePage):
    def load_admin_page(self, base_url: str) -> None:
        self.navigate(f"{base_url}/admin")

    def fill_login_form(self, username: str, password: str) -> None:
        self.page.get_by_role("textbox", name="Username").fill(username)
        self.page.get_by_role("textbox", name="Password").fill(password)

    def submit_login(self) -> None:
        self.page.get_by_role("button", name="Login").click()
        self.page.wait_for_url("**/admin**")

    def login(self, username: str, password: str) -> None:
        self.fill_login_form(username, password)
        self.submit_login()

    def room_form(self) -> Locator:
        return self.page.get_by_test_id("roomName")

    def invalid_login_alert(self) -> Locator:
        return self.page.get_by_text("Invalid credentials")

    def fill_room_form(
        self,
        roomName: str,
        type: str,
        accessible: str,
        roomPrice: int,
        features: list[str],
    ) -> None:
        self.page.get_by_test_id("roomName").fill(roomName)
        self.page.locator("#type").select_option(type)
        self.page.locator("#accessible").select_option(accessible)
        self.page.locator("#roomPrice").fill(str(roomPrice))

        for feature in features:
            self.page.get_by_role("checkbox", name=feature).check()

    def submit_new_room(self) -> None:
        self.page.get_by_role("button", name="Create").click()

    def new_room_created(self, room_number: str) -> Locator:
        return self.page.get_by_text(room_number)

    def open_room_page(self, room_name: str) -> None:
        self.page.locator('[data-testid="roomlisting"]').filter(has=self.page.locator(f"#roomName{room_name}")).click()

    def click_edit_button(self) -> None:
        self.page.get_by_role("button", name="Edit").click()

    def change_room_price(self, new_price: str) -> None:
        expect(self.page.get_by_role("textbox", name="Room price:")).not_to_be_empty()
        self.page.get_by_role("textbox", name="Room price:").fill(new_price)

    def click_update_button(self) -> None:
        self.page.get_by_role("button", name="Update").click()

    def room_price(self) -> Locator:
        return self.page.get_by_text("Room price:")

    def delete_room(self, room_number: str) -> None:
        self.page.locator('[data-testid="roomlisting"]').filter(has_text=room_number).locator("span.roomDelete").click()

    def room_to_delete(self, room_number: str) -> Locator:
        return self.page.locator(f"#roomName{room_number}")
