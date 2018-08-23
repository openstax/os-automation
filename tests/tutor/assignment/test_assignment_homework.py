"""Tests for instructors creating, modifying and deleting homeworks."""

from tests.markers import skip_test, test_case, tutor


@test_case('C208568')
@skip_test(reason='Script not written')
@tutor
def test_publish_a_new_homework_assignment(tutor_base_url, selenium, teacher):
    """Add a new homework assignment to an existing course."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN:  The user clicks on a date on the dashboard
    # AND: Click "add homework"
    # AND: Fill in all the required fields

    # THEN:  Click "Publish" button


@test_case('C208569')
@skip_test(reason='Script not written')
@tutor
def test_save_a_homework_draft(tutor_base_url, selenium, teacher):
    """Save a homework assignment as a draft."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Clicks on a date on the dashboard, then click "Add Homework"
    # AND: Fill in all the required fields
    # AND: Click "Save as Draft"

    # THEN: homework draft should be visible on the calendar


@test_case('C208570')
@skip_test(reason='Script not written')
@tutor
def test_edit_an_unopened_homework(tutor_base_url, selenium, teacher):
    """Edit and publish an unopened draft homework assignment."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Go to a course with unopened homework
    # AND: Click on an unopened homework
    # AND: Change all the required fields
    # AND: Click "publish"

    # THEN: User is taken back to the Calender
    # AND: The edits should be saved


@test_case('C208571')
@skip_test(reason='Script not written')
@tutor
def test_edit_an_opened_homework(tutor_base_url, selenium, teacher):
    """Edit an open homework assignment."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course with an open homework

    # WHEN: Go to a course with open homework
    # AND: Click on an opened homework
    # AND: Change all the required fields
    # AND: Click "Publish"

    # THEN: User is taken back to the Calender
    # AND: The edits should be saved


@test_case('C208572')
@skip_test(reason='Script not written')
@tutor
def test_cancel_editing_an_open_homework(tutor_base_url, selenium, teacher):
    """Cancel editing an opened homework assignment."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at a course with published homework

    # WHEN: Click on edit an published homework
    # AND: Change all the required fields
    # AND: Click "Cancel"

    # THEN: User is taken back to the Calender
    # AND: The edits should not be saved


@test_case('C208574')
@skip_test(reason='Script not written')
@tutor
def test_delete_an_open_homework(tutor_base_url, selenium, teacher):
    """Delete an opened homework assignment."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at a course with an opened homework

    # WHEN: Click on an opened homework
    # AND: Click "Delete"
    # AND: Click "Yes"

    # THEN: User is taken back to the Calender
    # AND: The homework should no longer be on the calender


@test_case('C208575')
@skip_test(reason='Script not written')
@tutor
def test_delete_an_unopened_homework(tutor_base_url, selenium, teacher):
    """Delete a published but unopened homework assignment."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at a course with an unopened homework

    # WHEN: Click on an unopened homework
    # AND: Click "Delete"
    # AND: Click "Yes"

    # THEN: User is taken back to the Calender
    # AND: The homework should no longer be on the calender


@test_case('C208576')
@skip_test(reason='Script not written')
@tutor
def test_delete_a_draft_homework(tutor_base_url, selenium, teacher):
    """Delete a draft homework assignment."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at a course with a homework draft

    # WHEN: Go to a course with homework draft
    # AND: Click on the homework draft
    # AND: Click "Delete"
    # AND: Click "Yes"

    # THEN: User is taken back to the Calender
    # AND: The homework draft should no longer be on the calender


@test_case('C208577')
@skip_test(reason='Script not written')
@tutor
def test_edit_a_draft_homework(tutor_base_url, selenium, teacher):
    """Modify a draft homework assignment."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at a course with a homework draft

    # WHEN: Click on edit a homework draft
    # AND: Change all the required fields
    # AND: Click "publish"

    # THEN: User is taken back to the Calender
    # AND: Edited draft with all info changed is published


@test_case('C210290')
@skip_test(reason='Script not written')
@tutor
def test_required_fields_for_homework_assignments(
        tutor_base_url, selenium, teacher):
    """Test fields required to save or publish a homework assignment."""
    # GIVEN: a user logged in as a teacher
    # AND: viewing the calendar dashboard for a course

    # WHEN: they open the "Add Assignment" pane
    # AND: click the "Add Homework" link
    # AND: click the "Publish" button

    # THEN: the "Assignment name", "Due date" and "Select Problems" field text
    #       are red
    # AND: "Required field" is displayed below the assignment name and due date
    #       fields and "Please select problems for this assignment." is below
    #       the select problems button
