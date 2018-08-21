"""Test the Tutor teacher course setting functions."""

from tests.markers import nondestructive, skip_test, test_case, tutor


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_change_course_name(tutor_base_url, selenium, teacher):
    """Change course name in course setting."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at the "Course Setting" page

    # WHEN: Click the pencil icon next to course name

    # THEN: a popup window for editing course name should appear
    # AND: user should be able to edit course name


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_switch_between_setting_tabs(tutor_base_url, selenium, teacher):
    """Switch between tabs in course setting."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at the "Course Setting" page

    # WHEN: Switch between "student access" and "dates and time" tabs

    # THEN: the content of the page should change accordingly


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_student_enrollment_url(tutor_base_url, selenium, teacher):
    """View student enrollment url for different sections."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Go to "Course Setting"

    # THEN: Student enrollment url for different sections should be present


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_change_course_time_zone(tutor_base_url, selenium, teacher):
    """Change course time zone in course settings."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at the ""Course Setting"" page

    # WHEN: Click the "dates and time" tab
    # AND: Click the pencil icon next to time zone

    # THEN: A popup window for changing the time zone should appear
    # AND: User should be able to change time zone in the popup window


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_cancel_changing_course_name(tutor_base_url, selenium, teacher):
    """Cancel changing course name in course settings."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at the "Course Setting" page

    # WHEN: Clicking the pencil icon next to course name
    # AND: Change the course name in the popup window
    # AND: Click x

    # THEN: Course name shouldn't change


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_cancel_changing_course_time_zone(tutor_base_url, selenium, teacher):
    """Cancel changing course time zone in course settings."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at the "Course Setting" page

    # WHEN: Click "dates and time"
    # AND: Click the pencil icon
    # AND: Change time zone selection
    # AND: Click x

    # THEN: Course time zone shouldn't change
