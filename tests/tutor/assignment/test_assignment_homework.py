"""Tests for instructors creating, modifying and deleting homeworks."""

from tests.markers import expected_failure, test_case, tutor


@test_case('')
@expected_failure
@tutor
def test_add_homework(tutor_base_url, selenium, teacher):
    """Test adding homework to a course."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN:  The user clicks on a date on the dashboard
    # AND: Click "add homework"
    # AND: Fill in all the required fields

    # THEN:  Click "Publish" button


@test_case('')
@expected_failure
@tutor
def test_add_homework_draft(tutor_base_url, selenium, teacher):
    """Test addomg homework draft to a course."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Clicks on a date on the dashboard, then click "Add Homework"
    # AND: Fill in all the required fields
    # AND: Click "Save as Draft"

    # THEN: homework draft should be visible on the calendar


@test_case('')
@expected_failure
@tutor
def test_publish_existing_unopened_homework(tutor_base_url, selenium, teacher):
    """Test publishing existing unopened homework."""
    # GIVEN: Logged into Tutor as a teacher

    # AND: Has an existing course

    # WHEN: The user goes to a course with unopened homework

    # AND: Click on an unopened hw

    # AND: Change all the required fields

    # AND: Click “publish"

    # THEN: User is taken back to the Calender

    # AND: The edits should be saved
