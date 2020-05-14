"""Test the Accounts home page."""

import pytest

from pages.accounts.home import AccountsHome as Home
from pages.accounts.reset import ChangePassword
from tests.markers import accounts, nondestructive, smoke_test, test_case
from utils.accounts import AccountsException
from utils.email import RestMail
from utils.utilities import Utility


@test_case('C195135')
@smoke_test
@nondestructive
@accounts
def test_open_the_accounts_home_page(accounts_base_url, selenium):
    """Basic start test."""
    # GIVEN: a user viewing the Accounts home page
    home = Home(selenium, accounts_base_url).open()

    # WHEN:

    # THEN: the Accounts Home page is displayed
    assert(home.menu.root.is_displayed()), 'Accounts header is not shown'
    assert(home.footer.root.is_displayed()), 'Accounts footer is not shown'

    # WHEN: they click the OpenStax logo
    web = home.menu.go_home()

    # THEN: the OpenStax.org web page is loaded
    assert('openstax.org' in web.location)


@test_case('C195136')
@smoke_test
@nondestructive
@accounts
def test_log_in_as_a_student(accounts_base_url, selenium, student):
    """Student log in test."""
    # GIVEN: a user viewing the Accounts Home page
    # AND:   valid credentials for a student user
    home = Home(selenium, accounts_base_url).open()

    # WHEN: the student user logs in
    profile = home.log_in(*student)

    # THEN: the student is logged in
    # AND: the student's profile is displayed
    assert('profile' in profile.location), f'User "{student[0]}" not logged in'

    assert(profile.content.title == "My Account"), 'Not viewing a profile'


@test_case('C195137')
@nondestructive
@accounts
def test_attempt_to_log_in_with_a_blank_user(accounts_base_url, selenium):
    """Blank username error message test."""
    # SETUP:
    user = ''
    password = ''

    # GIVEN: a user viewing the Accounts Home page
    home = Home(selenium, accounts_base_url).open()

    # WHEN: they click the "Continue" button
    with pytest.raises(AccountsException) as err:
        home.log_in(user, password)

    # THEN: an error message "Email can't be blank" is displayed
    assert("Email can't be blank" in str(err.value)), \
        'Incorrect error message'


@test_case('C195139')
@nondestructive
@accounts
def test_attempt_to_log_in_with_an_invalid_password(
        accounts_base_url, selenium, student):
    """Invalid password error message test."""
    # SETUP:
    user = student[0]
    password = ''

    # GIVEN: a user viewing the Accounts Home page
    home = Home(selenium, accounts_base_url).open()

    # WHEN: they enter the username or e-mail
    # AND:  enters an invalid password
    # AND:  clicks the "Continue" button
    with pytest.raises(AccountsException) as err:
        home.log_in(user, password)

    # THEN: an error message "Password can't be blank" is displayed
    assert("Password can't be blank" in str(err.value)), \
        'Incorrect error message'


@test_case('C195542')
@smoke_test
@accounts
def test_reset_a_users_password(accounts_base_url, selenium):
    """Reset a user's password."""
    # SETUP:
    name = Utility.random_name()
    email = RestMail(f'{name[1]}.{name[2]}.{Utility.random_hex(6)}'.lower())
    email.empty()
    address = email.address
    password = Utility.random_hex(length=14, lower=True)
    reset_password = Utility.random_hex(length=12, lower=True)

    # GIVEN: a registered user viewing the Accounts Home page
    home = Home(selenium, accounts_base_url).open()
    profile = home.student_signup(first_name=name[1], last_name=name[2],
                                  password=password, email=email)
    home = profile.content.log_out()
    email.empty()

    # WHEN: they click the "Forgot your password?" link
    # AND:  enter their email address
    # AND:  click the "Reset my password" button
    reset = home.content.forgot_your_password().content
    reset.email = address
    link_sent = reset.reset_my_password()

    # THEN: a "Password reset email sent" message is displayed
    assert('Password reset email sent' in link_sent.page_source), \
        f'Password reset message not seen ({link_sent.location})'

    # WHEN: open the "Reset your OpenStax password" e-mail
    # AND: click the "Click here to reset your OpenStax password." link
    # AND: a new password is entered in both input boxes
    # AND: click the "RESET PASSWORD" button
    # AND: click the "CONTINUE" button
    email.wait_for_mail()
    print(email.inbox[0].html)
    url = email.inbox[0].reset_link
    selenium.get(url)
    reset_form = ChangePassword(selenium, accounts_base_url).content
    reset_form.password = reset_password
    profile = reset_form.log_in()

    # THEN: the user's profile is displayed
    assert('profile' in profile.location), 'User is not logged in'

    # WHEN: the user logs out
    # AND: logs in using the new password
    home = profile.content.log_out()
    profile = home.log_in(address, reset_password)

    # THEN: the user's profile is displayed
    assert('profile' in profile.location), 'User is not logged in'


@test_case('C195142')
@nondestructive
@accounts
def test_view_the_accounts_copyright_notice(accounts_base_url, selenium):
    """View Accounts copyright notice."""
    # GIVEN: a user viewing the Accounts home page
    home = Home(selenium, accounts_base_url).open()

    # WHEN: they click the "Copyright © 2013-2020 Rice University"
    copyright = home.footer.view_copyright()

    # THEN: the Copyright and Licensing Details page is displayed
    assert('Copyright and Licensing' in copyright.page_source), \
        'Copyright not shown'


@test_case('C195143')
@nondestructive
@accounts
def test_view_the_accounts_terms_of_use(accounts_base_url, selenium):
    """View Accounts terms of use."""
    # GIVEN: a user viewing the Accounts home page
    home = Home(selenium, accounts_base_url).open()

    # WHEN: the "Terms of Use" link is clicked
    terms = home.footer.view_terms_of_use()

    # THEN: the "Site Terms & Policies" page is displayed
    assert('Site Terms' in terms.page_source), \
        'Terms of use not shown'


@test_case('C195144')
@nondestructive
@accounts
def test_go_to_the_rice_home_page(accounts_base_url, selenium):
    """Follow the Rice link."""
    # GIVEN: a user viewing the Accounts home page
    home = Home(selenium, accounts_base_url).open()

    # WHEN: they click the Rice University logo
    rice = home.footer.go_to_rice()

    # THEN: the Rice University web page is displayed
    assert(rice.at_rice)
    assert(selenium.title == 'Rice University'), \
        'Not at the Rice University webpage'


@test_case('C195543')
@nondestructive
@accounts
def test_go_to_account_signup(accounts_base_url, selenium):
    """Go to the account signup screen."""
    # GIVEN: a user viewing the Accounts home page
    home = Home(selenium, accounts_base_url).open()

    # WHEN: they click the "Sign up" tab
    signup = home.content.view_sign_up()

    # THEN: the account sign up page is displayed
    assert('signup' in signup.location), \
        'not viewing the user sign up page'
