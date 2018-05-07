"""Test the Accounts administrative pages."""
import os

import pytest
from pytest_testrail.plugin import testrail

from pages.accounts.admin import AccountsAdmin


@testrail('')
@pytest.mark.nondestructive
def test_admin_login(base_url, selenium):
    """Login as an administrator."""
    user = os.getenv('ADMIN_USER', '')
    password = os.getenv('ADMIN_PASSWORD', '')
    page = AccountsAdmin(selenium, base_url).open()
    assert(page)
    assert(not page.logged_in), 'Active user session unexpected'
    page.log_in(user, password)
    assert(page.logged_in), 'User "{0}" not logged in'.format(user)
