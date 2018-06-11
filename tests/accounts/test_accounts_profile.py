"""Test the Accounts logged in profile page."""

import os

import pytest

from pages.accounts.profile import AccountException, Profile
from pages.utils.utilities import Utility
from tests.markers import accounts, expected_failure, nondestructive  # noqa
from tests.markers import social, test_case  # noqa


@test_case('C195545')
@nondestructive
@accounts
def test_user_profile(accounts_base_url, selenium):
    """Login as a student user with a username."""
    page = Profile(selenium, accounts_base_url).open()
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


@test_case('C195546')
@nondestructive
@accounts
def test_admin_profile(accounts_base_url, selenium):
    """Login as an administrative user with a username."""
    page = Profile(selenium, accounts_base_url).open()
    assert(not page.logged_in), 'Active user session unexpected'
    username = os.getenv('ADMIN_USER')
    password = os.getenv('ADMIN_PASSWORD')
    page.log_in(username, password)
    assert(page.logged_in), 'User "{0}" not logged in'.format(username)
    assert(page.is_admin), 'User is not an administrator'
    assert(page.has_username), 'No username found'
    page.log_out()
    assert('/login' in selenium.current_url), 'Not at the Accounts login page'


@test_case('C195547')
@nondestructive
@accounts
def test_name_get_properties(accounts_base_url, selenium):
    """Test the getter methods for the name segments."""
    page = Profile(selenium, accounts_base_url).open()
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


@test_case('C195548')
@accounts
def test_profile_name_field(accounts_base_url, selenium):
    """Test the user's name field."""
    # setup
    page = Profile(selenium, accounts_base_url).open()
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


@test_case('C195551')
@accounts
def test_profile_username_field(accounts_base_url, selenium):
    """Test the user's username field."""
    # setup
    page = Profile(selenium, accounts_base_url).open()
    username = os.getenv('STUDENT_USER')
    password = os.getenv('STUDENT_PASSWORD')
    page.log_in(username, password)
    assert (page.logged_in), 'User is not logged in'
    # at profile, store original values
    old_username = page.username.username
    new_username = Utility.random_hex()
    # new_username = 'newuser'
    # set new values
    page.username.username = new_username
    assert (page.username.username != old_username), 'Username change failed'
    # reset the fields to the original values
    from time import sleep
    sleep(0.25)
    page.username.username = old_username
    sleep(0.25)
    assert (page.username.username == old_username), 'Username reset failed'


@test_case('C195552')
@nondestructive
@expected_failure
@accounts
def test_profile_email_fields(accounts_base_url, selenium):
    """Test the user's email fields."""


@test_case('C195554')
@expected_failure
@accounts
def test_verify_an_existing_unverified_email(accounts_base_url, selenium):
    """Test the user email verification process."""


@test_case('C195553')
@expected_failure
@accounts
def test_add_a_verified_email(accounts_base_url, selenium):
    """Test the ability to add an e-mail address to an existing user."""


@test_case('C195555')
@expected_failure
@accounts
@social
def test_profile_login_using_google(accounts_base_url, selenium):
    """Test the Gmail login method."""


@test_case('C195556')
@expected_failure
@accounts
@social
def test_profile_login_using_facebook(accounts_base_url, selenium):
    """Test the Facebook login method."""


@test_case('C195557')
@nondestructive
@expected_failure
@accounts
def test_admin_pop_up_console(accounts_base_url, selenium):
    """Test the pop up console."""


@test_case('C195558')
@nondestructive
@expected_failure
@accounts
def test_go_to_full_console(accounts_base_url, selenium):
    """Go to the full console."""
