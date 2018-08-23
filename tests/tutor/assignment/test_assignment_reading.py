"""Tests for instructors creating, modifying and deleting readings."""

from tests.markers import skip_test, test_case, tutor


@test_case('C208558', 'C208560', 'C208562', 'C208564')
@skip_test(reason='Script not written')
@tutor
def test_publish_edit_and_delete_a_new_reading(
        tutor_base_url, selenium, teacher):
    """Test the adding reading assignment."""
    # GIVEN: a user logged into Tutor as a teacher
    # AND: is viewing the calendar

    # WHEN: they click on a date on the dashboard
    # AND: click the "Add Reading" button
    # AND: fill out all of the form fields
    # AND: click the "Publish" button

    # THEN: the user is returned to the calendar
    # AND: the reading assignment is displayed
    # AND: the reading assignment is published

    # WHEN: the user clicks on the published reading
    # AND: clicks the "View Assignment" button
    # AND: edits one or more of the available fields
    # AND: clicks the "Save" button

    # THEN: the user is returned to the calendar
    # AND: the reading assignment is displayed
    # AND: the reading assignment is published
    # AND: the changes are saved

    # WHEN: the user clicks on the published reading
    # AND: clicks the "View Assignment" button
    # AND: edits one or more of the available fields
    # AND: clicks the "Cancel" button
    # AND: clicks the "Yes" button

    # THEN: the user is returned to the calendar
    # AND: the reading assignment is displayed
    # AND: the reading assignment is published
    # AND: the changes are not saved

    # WHEN: the user clicks on the published reading
    # AND: edits one or more of the available fields
    # AND: clicks the "x" button
    # AND: clicks the "Yes" button

    # THEN: the user is returned to the calendar
    # AND: the reading assignment is displayed
    # AND: the reading assignment is published
    # AND: the changes are not saved

    # WHEN: the user clicks on the published reading
    # AND: clicks the "View Assignment" button
    # AND: clicks the "Delete" button
    # AND: clicks the red "Delete" button

    # THEN: the user is returned to the calendar
    # AND: the reading assignment is removed from the calendar


@test_case('C208559', 'C208561', 'C208563', 'C208565')
@skip_test(reason='Script not written')
@tutor
def test_save_edit_and_delete_a_reading_draft(
        tutor_base_url, selenium, teacher):
    """Test adding, editing and deleting a reading assignment draft."""
    # GIVEN: a user logged into Tutor as a teacher
    # AND: is viewing the calendar

    # WHEN: they click on a date on the dashboard
    # AND: click the "Add Reading" button
    # AND: fill out all of the form fields
    # AND: click the "Save as Draft" button

    # THEN: the user is returned to the calendar
    # AND: the reading assignment is displayed
    # AND: the reading assignment name on the calendar is prefixed with "draft"

    # WHEN: the user clicks on the draft reading
    # AND: edits one or more of the available fields
    # AND: clicks the "Save as Draft" button

    # THEN: the user is returned to the calendar
    # AND: the reading assignment is displayed
    # AND: the reading assignment name on the calendar is prefixed with "draft"
    # AND: the changes are saved

    # WHEN: the user clicks on the draft reading
    # AND: edits one or more of the available fields
    # AND: clicks the "Cancel" button
    # AND: clicks the "Yes" button

    # THEN: the user is returned to the calendar
    # AND: the reading assignment is displayed
    # AND: the reading assignment name on the calendar is prefixed with "draft"
    # AND: the changes are not saved

    # WHEN: the user clicks on the draft reading
    # AND: clicks the "Cancel" button

    # THEN: the user is returned to the calendar
    # AND: the reading assignment is displayed
    # AND: the reading assignment name on the calendar is prefixed with "draft"
    # AND: the changes are not saved

    # WHEN: the user clicks on the draft reading
    # AND: edits one or more of the available fields
    # AND: clicks the "x" button
    # AND: clicks the "Yes" button

    # THEN: the user is returned to the calendar
    # AND: the reading assignment is displayed
    # AND: the reading assignment name on the calendar is prefixed with "draft"
    # AND: the changes are not saved

    # WHEN: the user clicks on the draft reading
    # AND: clicks the "x" button

    # THEN: the user is returned to the calendar
    # AND: the reading assignment is displayed
    # AND: the reading assignment name on the calendar is prefixed with "draft"
    # AND: the changes are not saved

    # WHEN: the user clicks on the draft reading
    # AND: clicks the "Delete" button
    # AND: clicks the red "Delete" button

    # THEN: the user is returned to the calendar
    # AND: the reading assignment is removed from the calendar


@test_case('C210289')
@skip_test(reason='Script not written')
@tutor
def test_required_fields_for_reading_assignments(
        tutor_base_url, selenium, teacher):
    """Test fields required to save or publish a reading assignment."""
    # GIVEN: a user logged in as a teacher
    # AND: viewing the calendar dashboard for a course

    # WHEN: they open the "Add Assignment" pane
    # AND: click the "Add Reading" link
    # AND: click the "Publish" button

    # THEN: the "Assignment name", "Due date" and "Add Readings" field text
    #       are red
    # AND: "Required field" is displayed below the assignment name and due date
    #      fields and "Please add readings to this assignment." is below the
    #      add readings button
