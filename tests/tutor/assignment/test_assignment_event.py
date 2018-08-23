"""Tests for instructors creating, modifying and deleting events."""

from tests.markers import skip_test, test_case, tutor


@test_case('C208587', 'C208589', 'C208592', 'C208593')
@skip_test(reason='Script not written')
@tutor
def test_tutor_publish_edit_and_delete_a_new_event(
        tutor_base_url, selenium, teacher):
    """Add a new event assignment, edit it, and delete it."""
    # GIVEN: a teacher logged into Tutor
    # AND: viewing the calendar dashboard for a course

    # WHEN: they click on a date on the dashboard
    # AND: click "add event"
    # AND: fill in all the required fields

    # TODO: list out fields to fill

    # AND: click the "Publish" button

    # THEN: the teacher is taken back to the calender
    # AND: a new event is visible on the calendar

    # WHEN: they click on a published event
    # AND: ...

    # TODO: deal with the quicklook view to edit it

    # AND: change all the required fields

    # TODO: list out fields to fill

    # AND: click the "Publish" button

    # THEN: the teacher is taken back to the calender
    # AND: the event is visible on the calendar with updated data

    # WHEN: they click on a published event
    # AND: ...

    # TODO: deal with the quicklook view to edit it

    # AND: change all the required fields

    # TODO: list out fields to fill

    # AND: click the "Cancel" button

    # THEN: the teacher is taken back to the Calender
    # AND: the event is visible on the calendar with pre-edit data

    # WHEN: they click on a published event
    # AND: ...

    # TODO: deal with the quicklook view to edit it

    # AND: click the "Delete" button
    # AND: click the "yes" button

    # THEN: the teacher is taken back to the calender
    # AND: the event is no longer be visible


@test_case('C208588', 'C208590', 'C208591', 'C208594')
@skip_test(reason='Script not written')
@tutor
def test_tutor_save_edit_and_delete_an_event_draft(
        tutor_base_url, selenium, teacher):
    """Add a new event draft, edit it, and delete it."""
    # GIVEN: a teacher logged into Tutor
    # AND: viewing the calendar dashboard for a course

    # WHEN: they click on a date on the dashboard
    # AND: click "add event"
    # AND: fill in all the required fields

    # TODO: list out fields to fill

    # AND: click the "Save as Draft" button

    # THEN: the teacher is taken back to the calender
    # AND: a new event draft is visible on the calendar

    # WHEN: they click on the event draft
    # AND: change all the required fields

    # TODO: list out fields to fill

    # AND: click the "Save" button

    # THEN: the teacher is taken back to the calender
    # AND: the event draft is visible on the calendar with updated data

    # WHEN: they click on an event draft
    # AND: change all the required fields

    # TODO: list out fields to fill

    # AND: click the "Cancel" button

    # THEN: the teacher is taken back to the calender
    # AND: the event is visible on the calendar with pre-edit data

    # WHEN: they click on the event draft
    # AND: click the "Delete" button
    # AND: click the "yes" button

    # THEN: the teacher is taken back to the calender
    # AND: the event is no longer visible


@test_case('C210288')
@skip_test(reason='Script not written')
@tutor
def test_required_fields_for_events(
        tutor_base_url, selenium, teacher):
    """Test fields required to save or publish an event."""
    # GIVEN: a user logged in as a teacher
    # AND: viewing the calendar dashboard for a course

    # WHEN: they open the "Add Assignment" pane
    # AND: click the "Add Event" link
    # AND: click the "Publish" button

    # THEN: the "Event name" and "Due date" field text are red
    # AND: "Required field" is displayed below the fields
