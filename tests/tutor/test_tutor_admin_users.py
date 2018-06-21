"""Test of admin console users page."""

from tests.markers import expected_failure, nondestructive, test_case, tutor


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_view_user_list(tutor_base_url, selenium, admin):
    """Test admin to view user list."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Users"" in the navbar

    # THEN: A list of users is displayed with a search bar
    # that allows an admin to find specific users


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_view_user_info(tutor_base_url, selenium, admin):
    """Test admin to view user info."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Users"" in the navbar
    # AND: Click on the ""Info"" button

    # THEN: User is taken to a page containing user info.
