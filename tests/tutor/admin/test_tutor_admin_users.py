"""Test of admin console users page."""

from tests.markers import nondestructive, skip_test, test_case, tutor


@test_case('C208732')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_view_user_list(tutor_base_url, selenium, admin):
    """View the Tutor user list."""
    # GIVEN: a user logged in as an administrative user
    # AND: viewing the admin console Users page

    # WHEN:

    # THEN: search bar is present
    # AND: a list of users is displayed that includes their status as an admin,
    #      customer service representative, content analyst and researcher
    # AND: buttons for editing, impersonating, and viewing the Tutor users
    #      exist


@test_case('C210280')
@skip_test(reason='Script not written')
@tutor
def test_edit_the_tutor_user_data(tutor_base_url, selenium, admin):
    """Edit a Tutor user."""
    # GIVEN: a user logged in as an administrative user
    # AND: viewing the admin console Users page

    # WHEN: they click the "Edit" button for a Tutor user
    # AND: change the username, first name, last name, full name, title, role,
    #      and account permissions
    # AND: clicks the "Save" button

    # THEN: the user is returned to the Users page
    # AND: the user data is changed
    # AND: the "The user has been updated." alert message is displayed

    # WHEN: the user reverts the changes

    # THEN: the original user data is restored


@test_case('C210281')
@skip_test(reason='Script not written')
@tutor
def test_impersonate_a_tutor_user(tutor_base_url, selenium, admin):
    """Impersonate a Tutor user."""
    # GIVEN: a user logged in as an administrative user
    # AND: viewing the admin console Users page

    # WHEN: they click the "Sign in as" button for a Tutor user

    # THEN: they are taken to the Tutor dashboard for the Tutor user
    # AND: they are logged in as that Tutor user


@test_case('C208733')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_view_a_tutor_users_information(tutor_base_url, selenium, admin):
    """View a Tutor user information screen."""
    # GIVEN: a user logged in as an administrative user
    # AND: viewing the admin console Users page

    # WHEN: they click the "Info" button for a Tutor user

    # THEN: user information is presented including their name, UUID, support
    #       identifier is set, status as a test account, and enrolled courses
    # AND: buttons for viewing the user's Accounts profile, editing the Tutor
    #      account, and impersonating the user exist


@test_case('C210282')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_search_for_a_tutor_user(tutor_base_url, selenium, admin):
    """Search for a Tutor user."""
    # GIVEN: a user logged in as an administrative user
    # AND: viewing the admin console Users page

    # WHEN: they enter "teacher" in the search bar
    # AND: click the "Search" button

    # THEN: users with "teacher" in their username or name are returned
    # AND: the results are paginated

    # WHEN: they enter a random hex number in the search bar
    # AND: click the "Search button"

    # THEN: no users are returned
    # AND: the "No users found." alert message is displayed
