"""Test the Accounts home page."""

import pytest

from pages.accounts.home import AccountsHome as Home
from tests.markers import accounts, nondestructive, smoke_test, test_case
from utils.email import RestMail
from utils.utilities import Utility


@test_case('C195135')
@smoke_test
@nondestructive
@accounts
def test_open_the_accounts_home_page(accounts_base_url, selenium):
    """Basic start test."""
    # GIVEN: A web browser

    # WHEN: Open the home page
    page = Home(selenium, accounts_base_url).open()

    # THEN: The Accounts Home page loads
    # AND: The OpenStax and Rice logos are displayed
    assert(page.header.is_header_displayed), 'Accounts header is not shown'
    assert(page.footer.is_footer_displayed), 'Accounts footer is not shown'
    page.header.go_to_accounts_home()
    assert(page.current_url == accounts_base_url + '/login')


@test_case('C195136')
@smoke_test
@nondestructive
@accounts
def test_log_in_as_a_student(accounts_base_url, selenium, student):
    """Student log in test."""
    # GIVEN: the Accounts Home page is open
    # AND: valid credentials for a student user
    page = Home(selenium, accounts_base_url).open()

    # WHEN: the student user logs in
    profile = page.log_in(*student)

    # THEN: the student is logged in
    # AND: the student's profile is displayed
    assert(profile.logged_in), 'User "{0}" not logged in'.format(student[0])
    assert(profile.title == "My Account"), 'Not viewing a profile'


@test_case('C195137')
@nondestructive
@accounts
def test_attempt_to_log_in_with_a_blank_user(accounts_base_url, selenium):
    """Blank username error message test."""
    # GIVEN: the Accounts Home page is loaded
    page = Home(selenium, accounts_base_url).open()
    user = ''
    password = ''

    # WHEN: the "NEXT" button is clicked
    with pytest.raises(AssertionError):
        page.log_in(user, password)

    # THEN: an error message "Username or email can't be blank" is displayed
    assert(page.login.get_login_error() ==
           "Username or email can't be blank"), \
        'Incorrect error message'


@test_case('C195138')
@nondestructive
@accounts
def test_attempt_to_log_in_with_an_invalid_user(accounts_base_url, selenium):
    """Unknown username error message test."""
    # GIVEN: the Accounts Home page is loaded
    page = Home(selenium, accounts_base_url).open()

    # WHEN: an invalid username is entered
    # AND: the "NEXT" button is clicked
    user = Utility().random_hex(20)
    password = ''
    with pytest.raises(AssertionError):
        page.log_in(user, password)

    # THEN: an error message "We don't recognize this username.
    #       Please try again or use your email address instead." is displayed
    assert('We don’t recognize this username.' in
           page.login.get_login_error()), \
        'Incorrect error message'


@test_case('C208850')
@nondestructive
@accounts
def test_attempt_to_log_in_with_an_invalid_email(accounts_base_url, selenium):
    """Attempt to log in with an invalid/unknown email address."""
    # GIVEN: the Accounts Home page is loaded
    page = Home(selenium, accounts_base_url).open()

    # WHEN: an invalid email address is entered
    # AND: the "NEXT" button is clicked
    user = Utility.fake_email(*Utility.random_name()[1:3])
    password = ''
    with pytest.raises(AssertionError):
        page.log_in(user, password)

    # THEN: an error message "We don't recognize this email. Please try again."
    #       is displayed
    assert('We don’t recognize this email.' in
           page.login.get_login_error()), \
        'Incorrect error message'


@test_case('C195139')
@nondestructive
@accounts
def test_attempt_to_log_in_with_an_invalid_password(
        accounts_base_url, selenium, student):
    """Invalid password error message test."""
    # GIVEN: the Accounts Home page is loaded
    # AND: a valid username or e-mail address
    page = Home(selenium, accounts_base_url).open()
    user = student[0]
    password = ''

    # WHEN: the username or e-mail is entered
    # AND: enters an invalid password
    # AND: clicks the "LOG IN" button
    with pytest.raises(AssertionError):
        page.log_in(user, password)

    # THEN: an error message "The password you provided is incorrect."
    #       is displayed# Enter a valid user but invalid password (blank)
    assert(page.login.get_login_error() ==
           'The password you provided is incorrect.'), \
        'Incorrect error message'


@test_case('C195542')
@smoke_test
@accounts
def test_reset_a_users_password(accounts_base_url, selenium, student):
    """Reset a user's password."""
    # GIVEN: a valid, accessible e-mail for a user
    # AND: at the Accounts Home page is loaded
    name = Utility.random_name()
    email = RestMail(
        '{first}.{last}.{tag}'
        .format(first=name[1], last=name[2], tag=Utility.random_hex(6))
        .lower()
    )
    email.empty()
    address = email.address
    password = student[1]
    reset_password = Utility.random_hex(length=12, lower=True)
    page = Home(selenium, accounts_base_url).open()
    page = page.login.go_to_signup.account_signup(
        email=address,
        password=password,
        _type='Student',
        provider='restmail',
        name=name,
        school='Automation',
        news=False)
    page.log_out()
    email.empty()

    # WHEN: the e-mail is entered in the input box
    # AND: click the "NEXT" button
    # AND: click the "Click here to reset it." link
    page.login.trigger_reset(address)

    # THEN: a "Check your email" text box is displayed
    assert('send_reset' in page.selenium.current_url and
           'Check your email' in page.selenium.page_source), \
        ('Check your email message not seen ({url})'
         .format(url=page.selenium.current_url))

    # WHEN: open the "Reset your OpenStax password" e-mail
    # AND: click the "Click here to reset your OpenStax password." link
    # AND: a new password is entered in both input boxes
    # AND: click the "RESET PASSWORD" button
    # AND: click the "CONTINUE" button
    email.wait_for_mail()
    url = email.inbox[0].reset_link
    page.login.reset_password(url, reset_password)

    # THEN: the user's profile is displayed
    assert(page.logged_in), 'User is not logged in'

    # WHEN: the user logs out
    # AND: logs in using the new password
    page.log_out()
    page.log_in(address, reset_password)

    # THEN: the user's profile is displayed
    assert(page.logged_in), 'User is not logged in'


@test_case('C195140')
@nondestructive
@accounts
def test_toggle_the_log_in_help_section(accounts_base_url, selenium):
    """Toggle the help section display."""
    # GIVEN: The Accounts Home page loads
    page = Home(selenium, accounts_base_url).open()

    # WHEN: The "Trouble logging in?" is clicked
    page.login.toggle_help

    # THEN: The help text is displayed
    assert(page.login.is_help_shown), 'Help text is not visible'

    # WHEN: The "Trouble logging in?" is clicked
    page.login.toggle_help

    # THEN: The help text is hidden
    assert(not page.login.is_help_shown), 'Help text is still visible'


@test_case('C195141')
@nondestructive
@accounts
def test_go_to_the_salesforce_help_pages(accounts_base_url, selenium):
    """Go to Salesforce help pages."""
    # GIVEN: the Accounts Home page is loaded
    page = Home(selenium, accounts_base_url).open()

    # WHEN: the "Trouble logging in?" link is clicked
    # AND: the "Visit our knowledge base for help" link is clicked
    salesforce = page.login.go_to_help

    # THEN: the "Can't log in to your OpenStax account?" help article is
    #       displayed in a new browser tab or window
    assert(salesforce.title == "Can’t log in to your OpenStax account?"), \
        'Not at the correct site or article'


@test_case('C195142')
@nondestructive
@accounts
def test_view_the_accounts_copyright_notice(accounts_base_url, selenium):
    """View Accounts copyright notice."""
    # GIVEN: the Accounts Home page is loaded
    page = Home(selenium, accounts_base_url).open()

    # WHEN: the "Copyright © 2013-2018 Rice University" link is clicked
    page.footer.show_copyright

    # THEN: the Copyright and Licensing Details page is displayed
    assert('Copyright and Licensing' in selenium.page_source), \
        'Copyright not shown'


@test_case('C195143')
@nondestructive
@accounts
def test_view_the_accounts_terms_of_use(accounts_base_url, selenium):
    """View Accounts terms of use."""
    # GIVEN: the Accounts Home page is loaded
    page = Home(selenium, accounts_base_url).open()

    # WHEN: the "Terms of Use" link is clicked
    page.footer.show_terms_of_use

    # THEN: the "Site Terms & Policies" page is displayed
    assert('Site Terms' in page.driver.page_source), \
        'Terms of use not shown'


@test_case('C195144')
@nondestructive
@accounts
def test_go_to_the_rice_home_page(accounts_base_url, selenium):
    """Follow the Rice link."""
    # GIVEN: the Accounts Home page is loaded
    page = Home(selenium, accounts_base_url).open()

    # WHEN: the Rice University logo is clicked
    rice = page.footer.go_to_rice()

    # THEN: the Rice University web page is displayed
    assert(rice.at_rice)
    assert(rice.driver.title == 'Rice University'), \
        'Not at the Rice University webpage'


@test_case('C195543')
@nondestructive
@accounts
def test_go_to_account_signup(accounts_base_url, selenium):
    """Go to the account signup screen."""
    # GIVEN: a web browser
    page = Home(selenium, accounts_base_url)

    # WHEN: go to the Accounts Home page
    # AND: the "Sign up here." link is clicked
    page.open()
    verify = page.login.go_to_signup

    # THEN: the "Sign up for an OpenStax account" page is displayed
    from pages.accounts.signup import Signup
    assert(isinstance(verify, Signup)), \
        'Signup object not returned'
    assert('signup' in verify.driver.current_url), \
        'Not at sign up page'
