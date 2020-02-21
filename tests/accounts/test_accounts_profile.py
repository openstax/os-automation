"""Test the Accounts logged in profile page."""

import pytest

from pages.accounts.home import AccountsHome
from tests.markers import accounts, nondestructive, skip_test, smoke_test, social, test_case  # NOQA
from utils.accounts import Accounts, AccountsException
from utils.email import RestMail
from utils.utilities import Utility


@test_case('C195545')
@smoke_test
@nondestructive
@accounts
def test_a_users_profile(accounts_base_url, selenium, student):
    """Login as a student user with a username."""
    # GIVEN: a valid student user viewing the Accounts home page
    home = AccountsHome(selenium, accounts_base_url).open()

    # WHEN: they log into Accounts
    profile = home.log_in(*student)

    # THEN: the user's profile is displayed
    # AND:  the admin console links are not displayed
    # AND:  the profile shows the name, username (if assigned), emails and log
    #       in methods
    assert('profile' in profile.location), f'User "{student[0]}" not logged in'
    assert(profile.content.root.is_displayed()), \
        'profile content not displayed'

    assert(not profile.console.is_admin), 'User is an administrator'
    with pytest.raises(AccountsException) as err:
        profile.console.view_popup_console()
    assert('not an administrator' in str(err.value)), \
        'pop up console displayed'

    assert(profile.content.name), "user's name not found"
    assert(profile.content.has_username), 'no username found'
    assert(profile.content.emails.emails), 'no email found'
    assert(profile.content.enabled_providers), 'no log in providers found'


@test_case('C195546')
@smoke_test
@nondestructive
@accounts
def test_an_administrators_profile(accounts_base_url, admin, selenium):
    """Login as an administrative user with a username."""
    # GIVEN: a valid administrative user viewing the Accounts home page
    home = AccountsHome(selenium, accounts_base_url).open()

    # WHEN: they log into Accounts
    profile = home.log_in(*admin)

    # THEN: the user's profile is displayed
    # AND:  the admin console links are displayed
    # AND:  the profile shows the name, username (if assigned), e-mails and log
    #       in methods
    assert('profile' in profile.location), f'User "{admin[0]}" not logged in'
    assert(profile.content.root.is_displayed()), \
        'profile content not displayed'

    assert(profile.console.is_admin), 'User is not an administrator'

    assert(profile.content.name), "user's name not found"
    assert(profile.content.has_username), 'no username found'
    assert(profile.content.emails.emails), 'no email found'
    assert(profile.content.enabled_providers), 'no log in providers found'


@test_case('C195547')
@nondestructive
@accounts
def test_get_the_user_name(accounts_base_url, selenium, student):
    """Test the name fields."""
    # GIVEN: a logged in student user viewing their profile
    home = AccountsHome(selenium, accounts_base_url).open()
    profile = home.log_in(*student)
    name = profile.content.name.full_name

    # WHEN: they open the name properties
    profile.content.name.change_name()
    getters = [
        profile.content.name.title,
        profile.content.name.first_name,
        profile.content.name.last_name,
        profile.content.name.suffix]

    # THEN: the user's full name matches the various name parts
    assert(name == ' '.join(getters).strip()), \
        'name does not match'


@test_case('C195548')
@accounts
def test_set_the_user_name(accounts_base_url, selenium, student):
    """Test the user's name field."""
    # SETUP:
    new_name = Utility.random_name()

    # GIVEN: a logged in student user viewing their profile
    home = AccountsHome(selenium, accounts_base_url).open()
    profile = home.log_in(*student)
    name = profile.content.name.get_name_parts()

    # WHEN: they changes their name
    profile.content.name.change_name()
    profile.content.name.title = new_name[Accounts.TITLE]
    profile.content.name.first_name = new_name[Accounts.FIRST]
    profile.content.name.last_name = new_name[Accounts.LAST]
    profile.content.name.suffix = new_name[Accounts.SUFFIX]
    profile.content.name.accept()

    # THEN: their name is changed
    assert(profile.content.name.full_name == ' '.join(new_name).strip()), \
        'the new name does not match'

    # WHEN: they resets the changes
    profile.content.name.change_name()
    profile.content.name.title = name[Accounts.TITLE]
    profile.content.name.first_name = name[Accounts.FIRST]
    profile.content.name.last_name = name[Accounts.LAST]
    profile.content.name.suffix = name[Accounts.SUFFIX]
    profile.content.name.accept()

    # THEN: their name is reset
    assert(profile.content.name.full_name == ' '.join(name).strip()), \
        'the name did not reset'


@test_case('C195551')
@accounts
def test_get_and_set_a_username(accounts_base_url, selenium, student):
    """Test the username field."""
    # SETUP:
    new_username = Utility.random_hex(18, True)

    # GIVEN: a user with a username viewing their profile
    home = AccountsHome(selenium, accounts_base_url).open()
    profile = home.log_in(*student)
    old_username = profile.content.username.username

    # WHEN: they click their username
    # AND:  enter a new username in the input field
    # AND:  click the checkmark button
    profile.content.username.change_username()
    profile.content.username.username = new_username
    profile.content.username.accept()

    # THEN: the username field shows the change
    assert (profile.content.username.username != old_username), \
        'username change failed'

    # WHEN: they click their username
    # AND:  enter the original username in the input field
    # AND:  click the checkmark button
    profile.content.username.change_username()
    profile.content.username.username = old_username
    profile.content.username.accept()

    # THEN: the original username is shown
    assert (profile.content.username.username == old_username), \
        'username reset failed'


@test_case('C195552')
@accounts
def test_get_current_emails_and_status(accounts_base_url, selenium, student):
    """Test the email fields."""
    # GIVEN: a student viewing their profile
    home = AccountsHome(selenium, accounts_base_url).open()
    profile = home.log_in(*student)

    # WHEN: they add a new email to the account
    name = profile.content.name.get_name_parts()
    fake_email = Utility.fake_email(name[Accounts.FIRST], name[Accounts.LAST])
    profile.content.emails.add_email_address()
    profile.content.emails.new_email.email = fake_email
    profile.content.emails.new_email.accept()

    # THEN: The new email is attached to the account
    status = False
    for entry in profile.content.emails.emails:
        status = status or (entry.email == fake_email)
    assert(status), f'"{fake_email}" not added'

    # WHEN: The new email is deleted
    for entry in profile.content.emails.emails:
        if entry.email == fake_email:
            popup = entry.delete()
            popup.ok()
            break

    # THEN: The email is removed from the account
    for entry in profile.content.emails.emails:
        assert(entry.email != fake_email), f'"{fake_email}" not removed'


@test_case('C195554')
@smoke_test
@accounts
def test_verify_an_email(accounts_base_url, selenium, student):
    """Test the email verification process."""
    # SETUP:
    name = Utility.random_hex(19, True)
    email = RestMail(name)
    email.empty()
    address = email.address

    # GIVEN: a student viewing their profile
    home = AccountsHome(selenium, accounts_base_url).open()
    profile = home.log_in(*student)

    # WHEN: they add an email without verifying it
    # AND:  click the email address
    # AND:  click the "Resend confirmation email" link
    # AND:  open the second verification email
    # AND:  click the confirmation link
    # AND:  close the new tab showing "Thank you for confirming your email
    #       address."
    # AND:  reload the profile page
    profile.content.emails.add_email_address()
    profile.content.emails.new_email.email = address
    profile.content.emails.new_email.accept()
    email.wait_for_mail()
    email.empty()
    for entry in profile.content.emails.emails:
        if entry.email == address:
            entry.toggle()
            entry.resend_confirmation_email()
    email.wait_for_mail()[-1].confirm_email()
    profile.reload()

    # THEN: the new email does not have "unconfirmed" to the right of it
    for entry in profile.content.emails.emails:
        if entry.email == address:
            assert(entry.is_confirmed), 'email is not confirmed'
            break

    # WHEN: they delete the new email
    for entry in profile.content.emails.emails:
        if entry.email == address:
            popup = entry.delete()
            profile = popup.ok()
            break

    # THEN: the email list is restored
    for entry in profile.content.emails.emails:
        assert(entry.email != address), 'email was not been removed'


@test_case('C195553')
@smoke_test
@accounts
def test_add_a_verified_email_to_profile(accounts_base_url, selenium, student):
    """Test the ability to add an e-mail address to an existing user."""
    # SETUP:
    name = Utility.random_hex(20, True)
    email = RestMail(name)
    email.empty()
    address = email.address

    # GIVEN: a student viewing their profile
    home = AccountsHome(selenium, accounts_base_url).open()
    profile = home.log_in(*student)

    # WHEN: they add an email
    # AND:  open the verification email
    # AND:  click the confirmation link
    # AND:  close the new tab showing "Thank you for confirming your email
    #       address."
    # AND:  reload the profile page
    profile.content.emails.add_email_address()
    profile.content.emails.new_email.email = address
    profile.content.emails.new_email.accept()
    email.wait_for_mail()[-1].confirm_email()
    profile.open()

    # THEN: the new email does not have "unconfirmed" to the right of it
    for entry in profile.content.emails.emails:
        if entry.email == address:
            assert(entry.is_confirmed), 'email is not confirmed'
            break

    # WHEN: they delete the new email
    for entry in profile.content.emails.emails:
        if entry.email == address:
            popup = entry.delete()
            profile = popup.ok()
            break

    # THEN: the email list is restored
    for entry in profile.content.emails.emails:
        assert(entry.email != address), 'email was not been removed'


@skip_test(reason='bypass social test')
@test_case('C195555')
@accounts
@social
def test_log_in_using_google(accounts_base_url, google, selenium):
    """Test the Gmail login method."""
    # GIVEN: a user with the Google authentication setup using a Gmail address
    # AND:   the Accounts Home page is loaded

    # WHEN: the user enters the Gmail address in the input
    # AND:  clicks the "NEXT" button
    # AND:  clicks the "Log in with Google" button

    # THEN: the user is taken to their profile


@skip_test(reason='bypass social test')
@test_case('C195556')
@accounts
@social
def test_log_in_using_facebook(accounts_base_url, facebook, selenium):
    """Test the Facebook login method."""
    # GIVEN: a user with the Facebook authentication setup using a Gmail
    #        address
    # AND:   the Accounts Home page is loaded

    # WHEN: the user enters the email address in the input
    # AND:  clicks the "NEXT" button
    # AND:  clicks the "Log in with Facebook" button

    # THEN: the user is taken to their profile


@test_case('C195557')
@smoke_test
@nondestructive
@accounts
def test_open_the_admin_pop_up_console(accounts_base_url, admin, selenium):
    """Open the pop up console modal."""
    # GIVEN: an admin viewing their profile
    home = AccountsHome(selenium, accounts_base_url).open()
    profile = home.log_in(*admin)

    # WHEN: they click the "Popup Console" link
    popup = profile.console.view_popup_console()

    # THEN: the pop up console is displayed
    assert(popup.root.is_displayed()), 'failed to open the popup console.'


@test_case('C195558')
@smoke_test
@nondestructive
@accounts
def test_go_to_the_admins_full_console(accounts_base_url, admin, selenium):
    """Open the full administrator console."""
    # GIVEN: an admin viewing their profile
    home = AccountsHome(selenium, accounts_base_url).open()
    profile = home.log_in(*admin)

    # WHEN: they click the "Full Console" link
    console = profile.console.view_full_console()

    # THEN: the admin control console is loaded
    assert('/admin/console' in selenium.current_url), \
        'not at the console page'
    assert(console.is_displayed()), 'full console not displayed'
