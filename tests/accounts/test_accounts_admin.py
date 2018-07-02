"""Test the Accounts administrative pages."""

from pages.accounts.admin import AccountsAdmin
from tests.markers import accounts, nondestructive, test_case


@test_case('C195544')
@nondestructive
@accounts
def test_admin_login(accounts_base_url, admin, selenium):
    """Login as an administrator."""
    page = AccountsAdmin(selenium, accounts_base_url).open()
    assert(page)
    assert(not page.logged_in), 'Active user session unexpected'
    page.log_in(*admin)
    assert(page.logged_in), 'User "{0}" not logged in'.format(admin[0])
