"""Test the Accounts home page."""
import os

import pytest
from pytest_testrail.plugin import testrail
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from pages.accounts.home import Home


@testrail('C195135')
@pytest.mark.nondestructive
def test_open_home_page(base_url, selenium):
    """Basic start test."""
    page = Home(selenium, base_url).open()
    assert(page)
    assert(page.header.is_header_displayed), 'Accounts header is not shown'
    assert(page.footer.is_footer_displayed), 'Accounts footer is not shown'
    page.header.go_to_accounts_home()
    assert(selenium.current_url == base_url + '/login')


@testrail('C195136')
@pytest.mark.nondestructive
def test_login_student(base_url, selenium):
    """Student login test."""
    user = os.getenv('STUDENT_USER', '')
    password = os.getenv('STUDENT_PASSWORD', '')
    page = Home(selenium, base_url).open()
    assert(not page.logged_in), 'Active user session unexpected'
    page.log_in(user, password)
    assert(page.logged_in), 'User "{0}" not logged in'.format(user)


@testrail('C195137')
@pytest.mark.nondestructive
def test_blank_login(base_url, selenium):
    """Blank username error message test.

    Username or email can't...
    """
    # Enter a blank username
    user = ''
    password = ''
    page = Home(selenium, base_url).open()
    with pytest.raises(NoSuchElementException):
        page.log_in(user, password)
    assert(page.login.get_login_error() ==
           "Username or email can't be blank"), \
        'Incorrect error message'


@testrail('C195138')
@pytest.mark.nondestructive
def test_unknown_login(base_url, selenium):
    """Unknown username error message test.

    We don't recognize this...
    """
    # Use a hex 20-digit number to generate an unknown username
    from random import randint
    hexdigits = '0123456789ABCDEF'
    user = ''.join([hexdigits[randint(0, 0xF)] for _ in range(20)])
    password = ''
    page = Home(selenium, base_url).open()
    with pytest.raises(NoSuchElementException):
        page.log_in(user, password)
    assert(page.login.get_login_error() ==
           "We don’t recognize this username. " +
           "Please try again or use your email address instead."), \
        'Incorrect error message'


@testrail('C195139')
@pytest.mark.nondestructive
def test_invalid_password(base_url, selenium):
    """Invalid password error message test.

    The password you provided...
    """
    # Enter a valid user but invalid password (blank)
    user = os.getenv('STUDENT_USER', '')
    password = ''
    page = Home(selenium, base_url).open()
    with pytest.raises(TimeoutException):
        page.log_in(user, password)
    assert(page.login.get_login_error() ==
           'The password you provided is incorrect.'), \
        'Incorrect error message'


@testrail('C195140')
@pytest.mark.nondestructive
def test_help_toggle(base_url, selenium):
    """Toggle the help section display."""
    page = Home(selenium, base_url).open()
    assert(not page.login.is_help_shown), 'Help text is already visible'
    page.login.toggle_help
    assert(page.login.is_help_shown), 'Help text is not visible'


@testrail('C195141')
@pytest.mark.nondestructive
def test_salesforce_link(base_url, selenium):
    """Go to Salesforce help pages."""
    page = Home(selenium, base_url).open()
    salesforce = page.login.go_to_help()
    salesforce.wait_for_page_to_load()
    assert(selenium.title == 'Salesforce Support page'), \
        'Not at the Salesforce help page'
    assert(salesforce.at_salesforce)


@testrail('C195142')
@pytest.mark.nondestructive
def test_copyright(base_url, selenium):
    """View Accounts copyright notice."""
    page = Home(selenium, base_url).open()
    page.footer.show_copyright
    assert('Copyright and Licensing' in selenium.page_source), \
        'Copyright not shown'


@testrail('C195143')
@pytest.mark.nondestructive
def test_terms_of_use(base_url, selenium):
    """View Accounts terms of use."""
    page = Home(selenium, base_url).open()
    page.footer.show_terms_of_use
    assert('Site Terms' in selenium.page_source), \
        'Terms of use not shown'


@testrail('C195144')
@pytest.mark.nondestructive
def test_go_to_rice(base_url, selenium):
    """Follow the Rice link."""
    page = Home(selenium, base_url).open()
    rice = page.footer.go_to_rice()
    assert(selenium.title == 'Rice University'), \
        'Not at the Rice University webpage'
    assert(rice.at_rice)
