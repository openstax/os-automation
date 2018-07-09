"""Test case for specific course dashboard."""

from tests.markers import expected_failure, nondestructive, test_case, tutor


@test_case('')
@expected_failure
@nondestructive
@tutor
def test_bypass_course_picker_page(tutor_base_url, selenium, student):
    """Test the tutor bypassing the course picker page."""
    # GIVEN: The Tutor home page logged in as a student

    # AND: The user has only one enrolled course

    # WHEN: The user logs in

    # THEN: The Dashboard page for the enrolled course loads


@test_case('')
@expected_failure
@nondestructive
@tutor
def test_return_to_dashboard_button(tutor_base_url, selenium, student):
    """Test the return to dashboard button."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a class

    # WHEN: The user goes into an enrolled class

    # AND: Click on "Return To Dashboard"

    # THEN: The dashboard loads


@test_case('')
@expected_failure
@tutor
def test_free_trial_nag(tutor_base_url, selenium, student):
    """Test the tutor assignment review."""
    # GIVEN: Logged into Tutor as a student

    # AND: Enrolled in a class with 14 days trial mode

    # WHEN:  The user goes to course with free trial

    # THEN: Free Trial Nag Includes a count-down on days left


@test_case('')
@expected_failure
@tutor
def test_full_access_to_trial(tutor_base_url, selenium, student):
    """Test the full trial payment from trial."""
    # GIVEN: Logged into Tutor as a student

    # AND: Enrolled in a class with 14 days trial mode

    # WHEN: The user goes to course with free trial

    # AND: Click on the "Get Access" button of the nag banner

    # THEN: User is taken to the payments page


@test_case('')
@expected_failure
@tutor
def test_free_trial_tag_disappear(tutor_base_url, selenium, student):
    """Test the free trial tag disappearing."""
    # GIVEN: Logged into Tutor as a student

    # AND: Enrolled in a class with 14 days trial mode

    # WHEN: The user pay for the course

    # AND: Refresh page

    # THEN: Free trial tag no longer there


@test_case('')
@expected_failure
@tutor
def test_preview_calendar(tutor_base_url, selenium, teacher):
    """Test the preview course calendar's assignment samples."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has a preview course

    # WHEN: The user goes to a preview course

    # THEN: From the calendar, the user should be able see sample assignments
    # and readings
