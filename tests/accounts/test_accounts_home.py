"""Test the Accounts home page."""

import os

import pytest
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from pages.accounts.home import AccountsHome as Home
from pages.utils.email import GuerrillaMail
from pages.utils.utilities import Utility
from tests.markers import accounts, expected_failure, nondestructive, test_case


@test_case('C195135')
@nondestructive
@accounts
def test_open_home_page(accounts_base_url, selenium):
    """Basic start test."""
    page = Home(selenium, accounts_base_url).open()
    assert(page)
    assert(page.header.is_header_displayed), 'Accounts header is not shown'
    assert(page.footer.is_footer_displayed), 'Accounts footer is not shown'
    page.header.go_to_accounts_home()
    assert(page.driver.current_url == accounts_base_url + '/login')


@test_case('C195136')
@nondestructive
@accounts
def test_login_student(accounts_base_url, selenium):
    """Student login test."""
    user = os.getenv('STUDENT_USER', '')
    password = os.getenv('STUDENT_PASSWORD', '')
    page = Home(selenium, accounts_base_url).open()
    assert(not page.logged_in), 'Active user session unexpected'
    page.log_in(user, password)
    assert(page.logged_in), 'User "{0}" not logged in'.format(user)


@test_case('C195137')
@nondestructive
@accounts
def test_blank_login(accounts_base_url, selenium):
    """Blank username error message test.

    Username or email can't...
    """
    # Enter a blank username
    user = ''
    password = ''
    page = Home(selenium, accounts_base_url).open()
    with pytest.raises(NoSuchElementException):
        page.log_in(user, password)
    assert(page.login.get_login_error() ==
           "Username or email can't be blank"), \
        'Incorrect error message'


@test_case('C195138')
@nondestructive
@accounts
def test_unknown_login(accounts_base_url, selenium):
    """Unknown username error message test.

    We don't recognize this...
    """
    # Use a hex 20-digit number to generate an unknown username
    user = Utility().random_hex(20)
    password = ''
    page = Home(selenium, accounts_base_url).open()
    with pytest.raises(NoSuchElementException):
        page.log_in(user, password)
    assert('We don’t recognize this username.' in
           page.login.get_login_error()), 'Incorrect error message'


@test_case('C195139')
@nondestructive
@accounts
def test_invalid_password(accounts_base_url, selenium):
    """Invalid password error message test.

    The password you provided...
    """
    # Enter a valid user but invalid password (blank)
    user = os.getenv('STUDENT_USER', '')
    password = ''
    page = Home(selenium, accounts_base_url).open()
    with pytest.raises(TimeoutException):
        page.log_in(user, password)
    assert(page.login.get_login_error() ==
           'The password you provided is incorrect.'), \
        'Incorrect error message'


@test_case('C195542')
@expected_failure
@accounts
def test_password_reset(accounts_base_url, selenium):
    """Reset a user's password."""
    # get a temporary e-mail
    page = GuerrillaMail(selenium).open()
    email = page.header.email
    old_password = Utility.random_hex(12)
    # sign up using the temporary e-mail and a random password
    page = Home(selenium, accounts_base_url).open()
    assert(not page.logged_in), 'Active user session unexpected'
    page.login.go_to_signup.account_signup(email=email, password=old_password)
    assert(page.logged_in), 'Failed to log in to Accounts'
    # reset a 'forgotten' password
    page.log_out()
    new_password = Utility.random_hex(12)
    page.reset_password(email, new_password)
    page.log_out()
    assert(not page.logged_in), 'Active user session unexpected'
    # try the new password
    page.log_in(email, new_password)
    assert(page.logged_in), 'Failed to log in to Accounts'


@test_case('C195140')
@nondestructive
@accounts
def test_help_toggle(accounts_base_url, selenium):
    """Toggle the help section display."""
    page = Home(selenium, accounts_base_url).open()
    assert(not page.login.is_help_shown), 'Help text is already visible'
    page.login.toggle_help
    assert(page.login.is_help_shown), 'Help text is not visible'


@test_case('C195141')
@nondestructive
@accounts
def test_salesforce_link(accounts_base_url, selenium):
    """Go to Salesforce help pages."""
    page = Home(selenium, accounts_base_url).open()
    salesforce = page.login.go_to_help
    salesforce.wait_for_page_to_load()
    assert(salesforce.driver.title == 'Salesforce Support page'), \
        'Not at the Salesforce help page'
    assert(salesforce.at_salesforce)


@test_case('C195142')
@nondestructive
@accounts
def test_copyright(accounts_base_url, selenium):
    """View Accounts copyright notice."""
    page = Home(selenium, accounts_base_url).open()
    page.footer.show_copyright
    assert('Copyright and Licensing' in selenium.page_source), \
        'Copyright not shown'


@test_case('C195143')
@nondestructive
@accounts
def test_terms_of_use(accounts_base_url, selenium):
    """View Accounts terms of use."""
    page = Home(selenium, accounts_base_url).open()
    page.footer.show_terms_of_use
    assert('Site Terms' in page.driver.page_source), \
        'Terms of use not shown'


@test_case('C195144')
@nondestructive
@accounts
def test_go_to_rice(accounts_base_url, selenium):
    """Follow the Rice link."""
    page = Home(selenium, accounts_base_url).open()
    rice = page.footer.go_to_rice()
    assert(rice.driver.title == 'Rice University'), \
        'Not at the Rice University webpage'
    assert(rice.at_rice)


@test_case('C195543')
@nondestructive
@accounts
def test_go_to_account_signup(accounts_base_url, selenium):
    """Go to the account signup screen."""
    from pages.accounts.signup import Signup
    page = Home(selenium, accounts_base_url).open()
    verify = page.login.go_to_signup
    assert(isinstance(verify, Signup)), \
        'Signup object not returned'
    assert('signup' in verify.driver.current_url), \
        'Not at sign up page'
