import pytest
from playwright.sync_api import Page, expect

from helpers import apply_field_rules, fake_price, fake_room
from pages.admin_page import AdminPage


@pytest.mark.admin
def test_valid_admin_login(page: Page, base_url, username, password):
    page_obj = AdminPage(page)
    page_obj.load_admin_page(base_url)
    page_obj.fill_login_form(username, password)
    page_obj.submit_login()
    expect(page_obj.room_form()).to_be_visible()


@pytest.mark.admin
def test_invalid_admin_login(page: Page, base_url, username):
    page_obj = AdminPage(page)
    page_obj.load_admin_page(base_url)
    page_obj.fill_login_form(username, "wrongPassword")
    page_obj.submit_login()
    expect(page_obj.invalid_login_alert()).to_be_visible()


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
    expect(page_obj.new_room_created(str(room_data["roomPrice"]))).to_be_visible()


@pytest.mark.admin
def test_edit_room_price(page: Page, base_url, username, password, create_room):
    new_price = str(fake_price())
    page_obj = AdminPage(page)
    page_obj.load_admin_page(base_url)
    page_obj.login(username, password)
    page_obj.open_room_page(create_room["name"])
    page_obj.click_edit_button()
    page_obj.change_room_price(new_price)
    page_obj.click_update_button()
    expect(page_obj.room_price()).to_contain_text(new_price)


@pytest.mark.admin
def test_delete_room(page: Page, base_url, username, password, create_room):
    page_obj = AdminPage(page)
    page_obj.load_admin_page(base_url)
    page_obj.login(username, password)
    page_obj.delete_room(create_room["name"])
    expect(page_obj.room_to_delete(create_room["name"])).not_to_be_visible()
