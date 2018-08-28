"""Test the Accounts logged in profile page."""

from functools import reduce

import pytest

from pages.accounts.profile import AccountException, Profile
from pages.utils.email import RestMail
from pages.utils.utilities import Utility
from tests.markers import accounts, expected_failure, nondestructive  # noqa
from tests.markers import skip_test, social, test_case  # noqa


@test_case('C195545')
@nondestructive
@accounts
def test_a_users_profile(accounts_base_url, selenium, student):
    """Login as a student user with a username."""
    # GIVEN: a valid student user login and password
    page = Profile(selenium, accounts_base_url).open()

    # WHEN: log into Accounts as the student
    page.log_in(*student)

    # THEN: the admin console links not displayed
    # AND: the profile shows the name, username if assigned, emails and log in
    #      methods
    assert(page.logged_in), 'User "{0}" not logged in'.format(student[0])
    assert(not page.is_admin), 'User is an administrator'
    assert(page.has_username), 'No username found'
    with pytest.raises(AccountException):
        page.open_popup_console()


@test_case('C195546')
@nondestructive
@accounts
def test_an_administrators_profile(accounts_base_url, admin, selenium):
    """Login as an administrative user with a username."""
    # GIVEN: a valid Accounts admin login and password
    page = Profile(selenium, accounts_base_url).open()

    # WHEN: log into Accounts as the admin
    page.log_in(*admin)

    # THEN: the admin console links are displayed
    # AND: the user's name, username if assigned, e-mails and log in methods
    #      are shown
    assert(page.logged_in), 'User "{0}" not logged in'.format(admin[0])
    assert(page.is_admin), 'User is not an administrator'
    assert(page.has_username), 'No username found'


@test_case('C195547')
@nondestructive
@accounts
def test_get_the_name_properties(accounts_base_url, selenium, student):
    """Test the getter methods for the name segments."""
    # GIVEN: A logged in student user
    page = Profile(selenium, accounts_base_url).open()
    page.log_in(*student)

    # WHEN: We request the user's full name
    # AND: We request the user's title, first name, surname and suffix
    name = page.name.full_name
    page.name.open()
    getters = [
        page.name.title,
        page.name.first_name,
        page.name.last_name,
        page.name.suffix]

    # THEN: The user's full name should match the various name parts
    assert(name == ' '.join(getters).strip()), \
        'Names do not match'


@test_case('C195548')
@accounts
def test_set_the_name_properties(accounts_base_url, selenium, student):
    """Test the user's name field."""
    # GIVEN: A logged in student user
    page = Profile(selenium, accounts_base_url).open()
    page.log_in(*student)
    name = page.name.get_name_parts()

    # WHEN: The user changes their name
    new_name = Utility.random_name()
    page.name.open()
    page.name.title = new_name[page.name.TITLE]
    page.name.first_name = new_name[page.name.FIRST]
    page.name.last_name = new_name[page.name.LAST]
    page.name.suffix = new_name[page.name.SUFFIX]
    page.name.confirm()

    # THEN: The user's name is changed
    assert(page.name.full_name == ' '.join(new_name).strip()), \
        'Names do not match'

    # WHEN: The user resets their name
    page.name.open()
    page.name.title = name[page.name.TITLE]
    page.name.first_name = name[page.name.FIRST]
    page.name.last_name = name[page.name.LAST]
    page.name.suffix = name[page.name.SUFFIX]
    page.name.confirm()

    # THEN: The user's name is reset
    assert(page.name.full_name == ' '.join(name).strip()), \
        'Names do not match'


@test_case('C195551')
@accounts
def test_get_and_set_a_username(accounts_base_url, selenium, student):
    """Test the user's username field."""
    # GIVEN: a user with a username
    # AND: viewing their profile
    page = Profile(selenium, accounts_base_url).open()
    page.log_in(*student)
    old_username = page.username.username
    new_username = Utility.random_hex()

    # WHEN: the username is clicked
    # AND: new text is entered in the input field
    # AND: the checkmark is clicked
    page.username.username = new_username

    # THEN: the username field shows the change
    assert (page.username.username != old_username), 'Username change failed'

    # WHEN: the username is clicked
    # AND: the original username is entered in the input field
    # AND: the checkmark is clicked
    page.username.username = old_username

    # THEN: the original username is shown
    assert (page.username.username == old_username), 'Username reset failed'


@test_case('C195552')
@accounts
def test_get_current_emails_and_status(accounts_base_url, selenium, student):
    """Test the user's email fields."""
    # GIVEN: a logged in student
    page = Profile(selenium, accounts_base_url).open()
    page.log_in(*student)

    # WHEN: the student adds a new email to the account
    name = page.name.get_name_parts()
    fake_email = Utility.fake_email(name[page.name.FIRST],
                                    name[page.name.LAST])
    page.emails.add_email(fake_email)

    # THEN: The new email is attached to the account
    assert(reduce(lambda x, y:
                  x or y.email_text == fake_email,
                  page.emails.emails,
                  False)), \
        'Email was not added'

    # WHEN: The new email is deleted
    for email in page.emails.emails:
        if email.email_text == fake_email:
            email.delete()
            break

    # THEN: The email is removed from the account
    assert(not reduce(lambda x, y: x or y.email_text == fake_email,
                      page.emails.emails,
                      False)), \
        'Email did not deleted properly'


@test_case('C195554')
@accounts
def test_verify_an_email(accounts_base_url, selenium, student):
    """Test the user email verification process."""
    # GIVEN: a student viewing their Accounts profile
    page = Profile(selenium, accounts_base_url).open()
    page.log_in(*student)
    initial_email_count = len(page.emails.emails)

    # WHEN: add an email without verifying the email
    # AND: clicks the email address
    # AND: clicks the "Resend confirmation email" link
    # AND: opens the second, verification email and click the confirmation link
    # AND: close the new tab showing "Thank you for confirming your email
    #      address."
    # AND: reload the profile page
    name = Utility.random_hex()
    restmail = RestMail(name)
    restmail.empty()
    address = name + '@restmail.net'
    page.emails.add_email(address)
    page.emails.emails[-1].resend_confirmation()
    restmail.wait_for_mail()[-1].confirm_email()
    page.open()

    # THEN: the new email does not have "unconfirmed" to the right of it
    assert(page.emails.emails[-1].is_confirmed), 'Email unconfirmed'

    # WHEN: delete the new email
    page.emails.emails[-1].delete()

    # THEN: the email list is restored
    assert(len(page.emails.emails) == initial_email_count), \
        'Email has not been removed'


@test_case('C195553')
@accounts
def test_add_a_verified_email_to_profile(accounts_base_url, selenium, student):
    """Test the ability to add an e-mail address to an existing user."""
    # GIVEN: a student viewing their Accounts profile
    page = Profile(selenium, accounts_base_url).open()
    page.log_in(*student)

    # WHEN: add an email
    # AND: opens the verification email and clicks the confirmation link
    # AND: closes the new tab showing "Thank you for confirming your email
    #      address."
    # AND: reload the profile page
    name = Utility.random_hex()
    restmail = RestMail(name)
    restmail.empty()
    address = name + '@restmail.net'
    page.emails.add_email(address)
    restmail.wait_for_mail()[-1].confirm_email()
    page.open()

    # THEN: the new email does not have "unconfirmed" to the right of it
    exists = False
    for email in page.emails.emails:
        if email.email_text == address:
            exists = True
            assert(email.is_confirmed), 'Email unconfirmed'
            break
    assert(exists), 'Email was not added'

    # WHEN: delete the new email
    for email in page.emails.emails:
        if email.email_text == address:
            email.delete()

    # THEN: the email list is restored
    assert(not reduce(lambda x, y: x or y.email_text == address,
                      page.emails.emails,
                      False)), \
        'Email did not deleted properly'


@test_case('C195555')
@accounts
@social
def test_log_in_using_google(accounts_base_url, google, selenium):
    """Test the Gmail login method."""
    # GIVEN: a user with the Google authentication setup using a Gmail address
    # AND: the Accounts Home page is loaded
    page = Profile(selenium, accounts_base_url).open()

    # WHEN: the user enters the Gmail address in the input
    # AND: clicks the "NEXT" button
    # AND: clicks the "Log in with Google" button
    page.login.google_login(google[0], *google)

    # THEN: the user is taken to their profile
    assert (page.logged_in), 'Failed to login with Google'


@test_case('C195556')
@accounts
@social
def test_log_in_using_facebook(accounts_base_url, facebook, selenium):
    """Test the Facebook login method."""
    # GIVEN: a user with the Facebook authentication setup using a Gmail
    #        address
    # AND: the Accounts Home page is loaded
    page = Profile(selenium, accounts_base_url).open()

    # WHEN: the user enters the email address in the input
    # AND: clicks the "NEXT" button
    # AND: clicks the "Log in with Facebook" button
    page.login.facebook_login(facebook[0], *facebook)

    # THEN: the user is taken to their profile
    assert (page.logged_in), 'Failed to login with facebook'


@test_case('C195557')
@nondestructive
@accounts
def test_open_the_admin_pop_up_console(accounts_base_url, admin, selenium):
    """Test the pop up console."""
    # GIVEN: an admin user logged into Accounts
    # AND: the Profile page is loaded
    page = Profile(selenium, accounts_base_url).open()
    page.log_in(*admin)

    # WHEN: the user clicks the "Popup Console" link
    page.open_popup_console()

    # THEN: the pop up console is displayed
    assert page.is_popup_console_displayed, 'Failed to open the popup console.'


@test_case('C195558')
@nondestructive
@accounts
def test_go_to_the_admins_full_console(accounts_base_url, admin, selenium):
    """Go to the full console."""
    # GIVEN: an admin user logged into Accounts
    # AND: the Profile page is loaded
    page = Profile(selenium, accounts_base_url).open()
    page.log_in(*admin)

    # WHEN: the user clicks the "Full Console" link
    page.open_full_console()

    # THEN: the admin control console page is loaded
    assert('/admin/console' in selenium.current_url), \
        'Not at the Full Admin Console page'
