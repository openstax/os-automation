"""Test of admin console notification page."""

from tests.markers import skip_test, test_case, tutor


@test_case('C208738')
@skip_test(reason='Script not written')
@tutor
def test_add_and_delete_a_new_general_notification(tutor_base_url,
                                                   selenium, admin):
    """Add and delete a general alert notification."""
    # GIVEN: a user logged in as an administrative user
    # AND: viewing the admin console Notifications page

    # WHEN: text is entered below the "New General Notification" input box
    # AND: the "From:" time is changed
    # AND: the "To:" time  is changed
    # AND: the "Add" button is clicked

    # THEN: a new general notification is created
    # AND: the "General notification created" alert is displayed

    # WHEN: the "Remove" button is clicked
    # AND: the alert box "OK" is clicked

    # THEN: the general notification is deleted
    # AND: the "General notification deleted" alert is displayed


@test_case('C208739')
@skip_test(reason='Script not written')
@tutor
def test_add_and_delete_a_new_instructor_only_notification(tutor_base_url,
                                                           selenium, admin):
    """Add and delete an instructor-only alert notification."""
    # GIVEN: a user logged in as an administrative user
    # AND: viewing the admin console Notifications page

    # WHEN: text is entered below the "New Instructor Notification" input box
    # AND: the "From:" time is changed
    # AND: the "To:" time  is changed
    # AND: the "Add" button is clicked

    # THEN: a new instructor notification is created
    # AND: the "Instructor notification created" alert is displayed

    # WHEN: the "Remove" button is clicked
    # AND: the alert box "OK" is clicked

    # THEN: the general notification is deleted
    # AND: the "Instructor notification deleted" alert is displayed
