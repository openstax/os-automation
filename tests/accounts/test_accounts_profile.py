"""Test the Accounts logged in profile page."""
import os

import pytest
from pytest_testrail.plugin import pytestrail

from pages.accounts.profile import AccountException
from pages.utils.utilities import Utility
from selenium.webdriver.common.by import By

try:
    from pages.accounts.profile import Profile
except ImportError:
    pass


@pytestrail.case('C195545')
@pytest.mark.nondestructive
def test_user_profile(base_url, selenium):
    """Login as a student user with a username."""
    page = Profile(selenium, base_url).open()
    assert(not page.logged_in), 'Active user session unexpected'
    username = os.getenv('STUDENT_USER')
    password = os.getenv('STUDENT_PASSWORD')
    page.log_in(username, password)
    assert(page.logged_in), 'User "{0}" not logged in'.format(username)
    assert(not page.is_admin), 'User is an administrator'
    assert(page.has_username), 'No username found'
    with pytest.raises(AccountException):
        page.open_popup_console()
    page.log_out()
    assert('/login' in selenium.current_url), 'Not at the Accounts login page'


@pytestrail.case('C195546')
@pytest.mark.nondestructive
def test_admin_profile(base_url, selenium):
    """Login as an administrative user with a username."""
    page = Profile(selenium, base_url).open()
    assert(not page.logged_in), 'Active user session unexpected'
    username = os.getenv('ADMIN_USER')
    password = os.getenv('ADMIN_PASSWORD')
    page.log_in(username, password)
    assert(page.logged_in), 'User "{0}" not logged in'.format(username)
    assert(page.is_admin), 'User is not an administrator'
    assert(page.has_username), 'No username found'
    page.log_out()
    assert('/login' in selenium.current_url), 'Not at the Accounts login page'


@pytestrail.case('C195547')
@pytest.mark.nondestructive
def test_name_get_properties(base_url, selenium):
    """Test the getter methods for the name segments."""
    page = Profile(selenium, base_url).open()
    username = os.getenv('STUDENT_USER')
    password = os.getenv('STUDENT_PASSWORD')
    page.log_in(username, password)
    assert(page.logged_in), 'User is not logged in'
    name = page.name.full_name()
    page.name.open()
    getters = [
        page.name.title,
        page.name.first_name,
        page.name.last_name,
        page.name.suffix]
    assert(name == ' '.join(getters).strip()), \
        'Names do not match'


@pytestrail.case('C195548')
def test_profile_name_field(base_url, selenium):
    """Test the user's name field."""
    # setup
    page = Profile(selenium, base_url).open()
    username = os.getenv('STUDENT_USER')
    password = os.getenv('STUDENT_PASSWORD')
    page.log_in(username, password)
    assert(page.logged_in), 'User is not logged in'
    # at profile, store original values
    page.name.open()
    name = page.name.get_name_parts()
    page.name.cancel()
    new_name = Utility.random_name()
    # set new values
    page.name.open()
    page.name.title = new_name[0]
    page.name.first_name = new_name[1]
    page.name.last_name = new_name[2]
    page.name.suffix = new_name[3]
    page.name.confirm()
    assert(page.name.full_name() == ' '.join(new_name).strip()), \
        'Names do not match'
    # reset the fields to the original values
    page.name.open()
    page.name.title = name[0]
    page.name.first_name = name[1]
    page.name.last_name = name[2]
    page.name.suffix = name[3]
    page.name.confirm()
    assert(page.name.full_name() == ' '.join(name).strip()), \
        'Names do not match'


@pytestrail.case('C195551')
@pytest.mark.xfail
def test_profile_username_field(base_url, selenium):
    """Test the user's username field."""


@pytestrail.case('C195552')
@pytest.mark.nondestructive
@pytest.mark.xfail
def test_profile_email_fields(base_url, selenium):
    """Test the user's email fields."""


@pytestrail.case('C195554')
@pytest.mark.xfail
def test_verify_an_existing_unverified_email(base_url, selenium):
    """Test the user email verification process."""


@pytestrail.case('C195553')
@pytest.mark.xfail
def test_add_a_verified_email(base_url, selenium):
    """Test the ability to add an e-mail address to an existing user."""


@pytestrail.case('C195555')
@pytest.mark.xfail
def test_profile_login_using_google(base_url, selenium):
    """Test the Gmail login method."""


@pytestrail.case('C195556')
@pytest.mark.xfail
def test_profile_login_using_facebook(base_url, selenium):
    """Test the Facebook login method."""


@pytestrail.case('C195557')
@pytest.mark.nondestructive
def test_admin_pop_up_console(base_url, selenium):
    page = Profile(selenium, base_url).open()
    assert(not page.logged_in), 'Active user session unexpected'
    username = os.getenv('ADMIN_USER')
    password = os.getenv('ADMIN_PASSWORD')
    page.log_in(username, password)
    assert(page.logged_in), 'User "{0}" not logged in'.format(username)
    assert(page.is_admin), 'User is not an administrator'
    assert(page.has_username), 'No username found'
    popup = page.open_popup_console()
    from time import sleep
    sleep(.25)
    misc = popup.misc
    assert(misc.task_locate())
    assert(misc.security_locate())
    assert(misc.routing_locate())
    assert(misc.controller_locate())
    assert(misc.action_locate())
    assert(misc.template_locate())
    assert(misc.not_yet_locate())
    #link of misc tests
    misc.task_locate().click()
    assert("cron" in selenium.current_url)

    popup = page.open_popup_console()
    sleep(.25)
    popup.misc.security_locate().click()
    assert("security_transgression" in selenium.current_url)
    # popup = page.open_popup_console()

    popup = page.open_popup_console()
    sleep(.25)
    popup.misc.routing_locate().click()
    assert("routing_error" in selenium.current_url)

    popup = page.open_popup_console()
    sleep(.25)
    popup.misc.controller_locate().click()
    assert("unknown_controller" in selenium.current_url)

    popup = page.open_popup_console()
    sleep(.25)
    popup.misc.action_locate().click()
    assert("unknown_action" in selenium.current_url)

    popup = page.open_popup_console()
    sleep(.25)
    popup.misc.template_locate().click()
    assert("missing_template" in selenium.current_url)

    popup = page.open_popup_console()
    sleep(.25)
    popup.misc.not_yet_locate().click()
    assert("not_yet_implemented" in selenium.current_url)

    #User
    popup = page.open_popup_console()
    sleep(.25)
    assert(popup.users.search_bar())
    assert(popup.users.search_button())

    #Links
    popup.links.search_security().click()
    assert("security_log" in selenium.current_url)

    selenium.back()
    popup = page.open_popup_console()
    sleep(.25)
    popup.links.search_application().click()
    assert("applications" in selenium.current_url)

    selenium.back()
    popup = page.open_popup_console()
    sleep(.25)
    popup.links.search_print().click()
    assert("print" in selenium.current_url)


    selenium.back()
    popup = page.open_popup_console()
    sleep(.25)
    popup.links.search_api().click()
    assert("api/docs/v1" in selenium.current_url)


    



    # assert(popup.find_element(By.CLASS_NAME, 'modal-open'))
    # page.find_element(By.CLASS_NAME, 'active').click()
    # assert(page.find_element(By.ID, "search_terms").is_displayed()), "Search bar not displayed"







@pytestrail.case('C195558')
@pytest.mark.nondestructive
@pytest.mark.xfail
def test_go_to_full_console(base_url, selenium):
    """Go to the full console."""
