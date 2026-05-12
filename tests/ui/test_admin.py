import pytest
from playwright.sync_api import Page

from helpers import apply_field_rules, fake_room
from pages.admin_page import AdminPage


@pytest.mark.admin
def test_valid_admin_login(page: Page, base_url, username, password):
    page_obj = AdminPage(page)
    page_obj.load_admin_page(base_url)
    page_obj.fill_login_form(username, password)
    page_obj.submit_login()
    page_obj.room_form_is_visible()


@pytest.mark.admin
def test_invalid_admin_login(page: Page, base_url, username):
    page_obj = AdminPage(page)
    page_obj.load_admin_page(base_url)
    page_obj.fill_login_form(username, "wrongPassword")
    page_obj.submit_login()
    page_obj.invalid_login_alert_is_visible()


@pytest.mark.admin
def test_create_new_room(page: Page, base_url, username, password, delete_room_after):
    room_data = apply_field_rules(fake_room(), exclude=["image", "description"])
    delete_room_after(room_data["roomName"])

    page_obj = AdminPage(page)
    page_obj.load_admin_page(base_url)
    page_obj.fill_login_form(username, password)
    page_obj.submit_login()
    page_obj.fill_room_form(**room_data)
    page_obj.submit_new_room()
    page_obj.new_room_is_created(str(room_data["roomPrice"]))


@pytest.mark.admin
def test_edit_room_price(page: Page, base_url, username, password, create_room):
    new_price = "220"
    page_obj = AdminPage(page)
    page_obj.load_admin_page(base_url)
    page_obj.login(username, password)
    page_obj.click_room_entry(create_room)
    page_obj.click_edit_button()
    page_obj.change_room_price(new_price)
    page_obj.click_update_button()
    page_obj.room_price_is(new_price)


@pytest.mark.admin
def test_delete_room(page: Page, base_url, username, password, create_room):
    page_obj = AdminPage(page)
    page_obj.load_admin_page(base_url)
    page_obj.login(username, password)
    page_obj.delete_room(create_room)
    page_obj.room_is_not_in_list(create_room)
