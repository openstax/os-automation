"""Test the Accounts logged in profile page."""

import pytest

from pages.accounts.profile import AccountException, Profile
from pages.utils.email import GuerrillaMail
from pages.utils.utilities import Utility
from tests.markers import accounts, expected_failure, nondestructive  # noqa
from tests.markers import social, test_case  # noqa


@test_case('C195545')
@nondestructive
@accounts
def test_user_profile(accounts_base_url, selenium, student):
    """Login as a student user with a username."""
    page = Profile(selenium, accounts_base_url).open()
    assert(not page.logged_in), 'Active user session unexpected'
    page.log_in(*student)
    assert(page.logged_in), 'User "{0}" not logged in'.format(student[0])
    assert(not page.is_admin), 'User is an administrator'
    assert(page.has_username), 'No username found'
    with pytest.raises(AccountException):
        page.open_popup_console()
    page.log_out()
    assert('/login' in selenium.current_url), 'Not at the Accounts login page'


@test_case('C195546')
@nondestructive
@accounts
def test_admin_profile(accounts_base_url, admin, selenium):
    """Login as an administrative user with a username."""
    page = Profile(selenium, accounts_base_url).open()
    assert(not page.logged_in), 'Active user session unexpected'
    page.log_in(*admin)
    assert(page.logged_in), 'User "{0}" not logged in'.format(admin[0])
    assert(page.is_admin), 'User is not an administrator'
    assert(page.has_username), 'No username found'
    page.log_out()
    assert('/login' in selenium.current_url), 'Not at the Accounts login page'


@test_case('C195547')
@nondestructive
@accounts
def test_name_get_properties(accounts_base_url, selenium, student):
    """Test the getter methods for the name segments."""
    page = Profile(selenium, accounts_base_url).open()
    page.log_in(*student)
    assert(page.logged_in), 'User is not logged in'
    name = page.name.full_name()
    page.name.open()
    getters = [
        page.name.title,
        page.name.first_name,
        page.name.last_name,
        page.name.suffix]
    assert(name == ' '.join(getters).strip()), \
        'Names do not match'


@test_case('C195548')
@accounts
def test_profile_name_field(accounts_base_url, selenium, student):
    """Test the user's name field."""
    # setup
    page = Profile(selenium, accounts_base_url).open()
    page.log_in(*student)
    assert(page.logged_in), 'User is not logged in'
    # at profile, store original values
    page.name.open()
    name = page.name.get_name_parts()
    page.name.cancel()
    new_name = Utility.random_name()
    # set new values
    page.name.open()
    page.name.title = new_name[0]
    page.name.first_name = new_name[1]
    page.name.last_name = new_name[2]
    page.name.suffix = new_name[3]
    page.name.confirm()
    assert(page.name.full_name() == ' '.join(new_name).strip()), \
        'Names do not match'
    # reset the fields to the original values
    page.name.open()
    page.name.title = name[0]
    page.name.first_name = name[1]
    page.name.last_name = name[2]
    page.name.suffix = name[3]
    page.name.confirm()
    assert(page.name.full_name() == ' '.join(name).strip()), \
        'Names do not match'


@test_case('C195551')
@accounts
def test_profile_username_field(accounts_base_url, selenium, student):
    """Test the user's username field."""
    # setup
    page = Profile(selenium, accounts_base_url).open()
    page.log_in(*student)
    assert (page.logged_in), 'User is not logged in'
    # at profile, store original values
    old_username = page.username.username
    new_username = Utility.random_hex()
    # set new values
    page.username.username = new_username
    assert (page.username.username != old_username), 'Username change failed'
    # reset the fields to the original values
    page.username.username = old_username
    assert (page.username.username == old_username), 'Username reset failed'


@test_case('C195552')
@nondestructive
@accounts
def test_profile_email_fields(accounts_base_url, selenium, student):
    """Test the user's email fields."""
    # setup
    page = Profile(selenium, accounts_base_url).open()
    page.log_in(*student)
    assert(page.logged_in), 'User is not logged in'
    # add a new email
    prelen = len(page.emails.emails)
    page.emails.add_email()
    pastlen = len(page.emails.emails)
    assert (pastlen == prelen + 1), "Email is not added properly"
    # delete the new email added
    email = page.emails.emails[-1]
    email.delete()
    finallen = len(page.emails.emails)
    assert (pastlen == finallen + 1), "Email is not deleted properly"


@test_case('C195554')
@expected_failure
@accounts
def test_verify_an_existing_unverified_email(accounts_base_url, selenium,
                                             student):
    """Test the user email verification process."""
    # GIVEN the user is valid and has a existing unverified email
    page = GuerrillaMail(selenium).open()
    email = page.header.email
    assert email is not None, "Didn't get guerrilla email"
    page = Profile(page.driver).open()
    page.log_in(*student)
    page.emails.add_email(email)
    new_email = page.emails.emails.pop()

    # WHEN the user click resend confirmation
    new_email.resend_confirmation()

    # THEN the user should receive new confirmation email
    page = GuerrillaMail(page.driver, timeout=60).open()
    page.wait_for_email()
    assert len(page.emails) > 2, "Didn't receive email"
    new_email = page.emails[0]
    new_email.open_email()

    # WHEN the user click the confirmation link
    page.openedmail.confirm_email()
    assert 'openstax.org/confirm?' in selenium.current_url

    # THEN the email should appear as confirmed
    page = Profile(page.driver).open()
    new_email = page.emails.emails.pop()
    assert new_email.is_confirmed, "The email isn't verified"


@test_case('C195553')
@accounts
def test_add_a_verified_email(accounts_base_url, selenium, student):
    """Test the ability to add an e-mail address to an existing user."""
    # GIVEN the user is valid

    # WHEN the user add a new email
    page = GuerrillaMail(selenium).open()
    email = page.header.email
    assert email is not None, "Didn't get guerrilla email"
    page = Profile(page.driver).open()
    page.log_in(*student)
    page.emails.add_email(email)

    # THEN the user should receive a confirmation email automatically
    page = GuerrillaMail(page.driver, timeout=60).open()
    page.wait_for_email()
    assert len(page.emails) > 1, "Didn't receive email"
    new_email = page.emails[0]
    new_email.open_email()

    # WHEN the user click the confirmation link
    page.openedmail.confirm_email()
    assert 'openstax.org/confirm?' in selenium.current_url

    # THEN the email should appear as confirmed
    page = Profile(page.driver).open()
    new_email = page.emails.emails.pop()
    assert new_email.is_confirmed, "The email isn't verified"


@test_case('C195555')
@accounts
@social
def test_profile_login_using_google(accounts_base_url, google, selenium,
                                    student):
    """Test the Gmail login method."""
    # GIVEN the user had added Google as an alternative login method
    # AND the user is not logged in
    page = Profile(selenium, accounts_base_url).open()
    assert(not page.logged_in), 'Already logged in'

    # WHEN the user logs into OpenStax through a Google account
    page.login.google_login(student[0], *google)

    # THEN the user is logged in
    assert (page.logged_in), 'Failed to login with google'


@test_case('C195556')
@accounts
@social
def test_profile_login_using_facebook(accounts_base_url, facebook, selenium,
                                      student):
    """Test the Facebook login method."""
    # GIVEN the user had added Facebook as an alternative login method
    # AND the user is not logged in
    page = Profile(selenium, accounts_base_url).open()
    assert(not page.logged_in), 'Already logged in'

    # WHEN the user logs into OpenStax through a Facebook account
    page.login.facebook_login(student[0], *facebook)

    # THEN the user is logged in
    assert (page.logged_in), 'Failed to login with facebook'


@test_case('C195557')
@nondestructive
@accounts
def test_admin_pop_up_console(accounts_base_url, admin, selenium):
    """Test the pop up console."""
    page = Profile(selenium, accounts_base_url).open()
    assert(not page.logged_in), 'Active user session unexpected'
    page.log_in(*admin)
    assert(page.logged_in), 'User "{0}" not logged in'.format(admin[0])
    assert(page.is_admin), 'User is not an administrator'
    assert(page.has_username), 'No username found'
    popup = page.open_popup_console()

    misc = popup.misc
    assert(misc.task_locate())
    assert(misc.security_locate())
    assert(misc.routing_locate())
    assert(misc.controller_locate())
    assert(misc.action_locate())
    assert(misc.template_locate())
    assert(misc.not_yet_locate())
    # link of misc tests
    misc.task_locate().click()
    assert("cron" in selenium.current_url)

    popup = page.open_popup_console()
    popup.misc.security_locate().click()
    assert("security_transgression" in selenium.current_url)

    popup = page.open_popup_console()
    popup.misc.routing_locate().click()
    assert("routing_error" in selenium.current_url)

    popup = page.open_popup_console()
    popup.misc.controller_locate().click()
    assert("unknown_controller" in selenium.current_url)

    popup = page.open_popup_console()
    popup.misc.action_locate().click()
    assert("unknown_action" in selenium.current_url)

    popup = page.open_popup_console()
    popup.misc.template_locate().click()
    assert("missing_template" in selenium.current_url)

    popup = page.open_popup_console()
    popup.misc.not_yet_locate().click()
    assert("not_yet_implemented" in selenium.current_url)

    # User
    popup = page.open_popup_console()
    assert(popup.users.search_bar())
    assert(popup.users.search_button())

    # Links
    popup.links.search_security().click()
    assert("security_log" in selenium.current_url)

    selenium.back()
    popup = page.open_popup_console()
    popup.links.search_application().click()
    assert("applications" in selenium.current_url)

    selenium.back()
    popup = page.open_popup_console()
    popup.links.search_print().click()
    assert("print" in selenium.current_url)

    selenium.back()
    popup = page.open_popup_console()
    popup.links.search_api().click()
    assert("api/docs/v1" in selenium.current_url)


@test_case('C195558')
@nondestructive
@accounts
def test_go_to_full_console(accounts_base_url, admin, selenium):
    """Go to the full console."""
    # GIVEN the user is logged in as an administrator
    page = Profile(selenium, accounts_base_url).open()
    assert(not page.logged_in), 'User is not logged in'
    page.log_in(*admin)
    assert(page.logged_in), 'User is not logged in'
    assert(page.is_admin), 'User is not an administrator'

    # WHEN the user clicks the full console
    page.open_full_console()

    # THEN the user is routed to the full console page
    assert('/admin/console' in selenium.current_url), \
        'Not at the Full Admin Console page'
