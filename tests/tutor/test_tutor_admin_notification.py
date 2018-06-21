"""Test of admin console notification page."""

from tests.markers import expected_failure, nondestructive, test_case, tutor


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_add_notification(tutor_base_url, selenium, admin):
    """Test admin to add notification."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""System Settings"" in the navbar
    # AND: In the drop down click on ""Notifications""
    # AND: Choose either ""General Notifications"" or
    # ""Instructor Notifications"" and fill out the necessary fields
    # AND: Click ""Add""

    # THEN: A new notification is created.


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_delete_notification(tutor_base_url, selenium, admin):
    """Test admin to delete notification."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""System Settings"" in the navbar
    # AND: In the drop down click on ""Notifications""
    # AND: Click ""Remove"" next to a current notification

    # THEN: The notification is removed from the notification list.
