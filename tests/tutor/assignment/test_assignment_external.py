"""Tests for instructors creating, modifying and deleting externals."""

from tests.markers import skip_test, test_case, tutor


@test_case('C208578', 'C208580', 'C208584', 'C208582')
@skip_test(reason='Script not written')
@tutor
def test_publish_edit_and_delete_a_new_external_assignment(
        tutor_base_url, selenium, teacher):
    """Test publishing, editing and deleting an external assignment."""
    # GIVEN: Logged into Tutor as a teacher

    # WHEN: click a date on the dashboard, then click "add external assignment"
    # AND: fill in all the required fields
    # AND: click "Publish"

    # THEN: User is taken back to the Calender
    # AND: A new reading assignment should be visible on calender

    # WHEN: Click on edit the external assignment
    # AND: Change all the required fields
    # AND: Click "publish"

    # THEN: User is taken back to the Calender
    # AND: An edited external assignment is visible on calendar

    # WHEN: Click on an external assignment.
    # AND: Change all the required fields
    # AND: Click “cancel"

    # THEN: User is taken back to the Calender
    # AND: No changes should be made on the assignment

    # WHEN: Click on an external assignment
    # AND: Click “delete"
    # AND: Click "yes"

    # THEN: User is taken back to the Calender
    # AND: The external assignment is no longer visible on the calendar"


@test_case('C208579', 'C208581', 'C208585', 'C208583')
@skip_test(reason='Script not written')
@tutor
def test_save_edit_and_delete_a_new_draft_external_assignment(
        tutor_base_url, selenium, teacher):
    """Test saving, editing and deleting an external assignment."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click a date on the dashboard, then click "add external assignment"
    # AND: Fill in all the required fields
    # AND: Click “save as draft

    # THEN: User is taken back to the Calender
    # AND: A new reading draft should be visible on calender

    # WHEN: Click on edit an external assignment draft
    # AND: Change all the required fields
    # AND: Click “publish"

    # THEN: User is taken back to the Calender
    # AND: Edited draft is published"

    # WHEN: Click on edit an external assignment draft
    # AND: Change all the required fields
    # AND: Click “Cancel"

    # THEN: User is taken back to the Calender
    # AND: No changes should be made on the draft

    # WHEN: Click on an external assignment draft
    # AND: Click "delete"
    # AND: Click "yes"

    # THEN: User is taken back to the Calender
    # AND: The draft is deleted and no longer visible on the calendar


@test_case('C208586')
@skip_test(reason='Script not written')
@tutor
def test_required_fields_for_external_assignments(
        tutor_base_url, selenium, teacher):
    """Test fields required to save or publish an external assignment."""
    # GIVEN: a user logged in as a teacher
    # AND: viewing the calendar dashboard for a course

    # WHEN: they open the "Add Assignment" pane
    # AND: click the "Add External Assignment" link
    # AND: click the "Publish" button

    # THEN: the "Assignment name", "Due Date" and "Assignment URL" field text
    #       are red
    # AND: "Required field" is displayed below the assignment name, due date,
    #       and URL fields
