"""Test the Accounts logged in profile page."""
import os

import pytest
from pytest_testrail.plugin import testrail

from pages.accounts.profile import AccountException, Profile

USERNAME = os.getenv('STUDENT_USER', '')
PASSWORD = os.getenv('STUDENT_PASSWORD', '')


@testrail('')
@pytest.mark.nondestructive
def test_user_profile(base_url, selenium):
    """Login as an administrator."""
    page = Profile(selenium, base_url).open()
    assert(page)
    assert(not page.logged_in), 'Active user session unexpected'
    page.log_in(USERNAME, PASSWORD)
    assert(page.logged_in), 'User "{0}" not logged in'.format(USERNAME)
    assert(not page.is_admin), 'User is an administrator'
    assert(page.has_username), 'No username found'
    with pytest.raises(AccountException):
        page.open_popup_console()
    page.log_out()
    assert('/login' in selenium.current_url), 'Not at the Accounts login page'
