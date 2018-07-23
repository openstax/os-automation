"""Test the Accounts administrative pages."""

from pages.accounts.admin import AccountsAdmin
from tests.markers import accounts, nondestructive, test_case


@test_case('C195544')
@nondestructive
@accounts
def test_admin_login(accounts_base_url, admin, selenium):
    """Log in as an administrator."""
    # GIVEN: a valid Accounts administrative login and password

    # WHEN: the admin opens the Accounts Home page
    # AND: logs into Accounts
    page = AccountsAdmin(selenium, accounts_base_url).open()
    page.log_in(*admin)

    # THEN: the administrator is logged in
    assert(page.logged_in), 'User "{0}" not logged in'.format(admin[0])
    assert(page.is_admin), 'User is not an administrator'
