"""Test the Tutor teacher course calendar functions."""

from tests.markers import expected_failure, nondestructive, test_case, tutor


@expected_failure
@test_case('')
@tutor
def test_edit_an_unopened_homework(tutor_base_url, selenium, teacher):
    """Edit an unopened homework."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course with an open homework

    # WHEN: Go to a course with unopened homework
    # AND: Click on an unopened homework
    # AND: Change all the required fields
    # AND: Click "publish"

    # THEN: User is taken back to the Calendar
    # AND: The edits should be saved


@expected_failure
@test_case('')
@tutor
def test_edit_an_opened_homework(tutor_base_url, selenium, teacher):
    """Edit an opened homework."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course with an open homework

    # WHEN: Go to a course with open homework
    # AND: Click on an opened homework
    # AND: Change all the required fields
    # AND: Click "Publish"

    # THEN: User is taken back to the Calender
    # AND: The edits should be saved


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_cancel_edit_homework(tutor_base_url, selenium, teacher):
    """Cancel editing a published homework."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course with an published homework
    # WHEN: Go to a course with published homework
    # AND: Click on an published homework
    # AND: Change all the required fields
    # AND: Click "Cancel"

    # THEN: User is taken back to the Calender
    # AND: The edits should not be saved


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_cancel_edit_draft(tutor_base_url, selenium, teacher):
    """Cancel editing a published homework draft."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: has an existing homework draft

    # WHEN: Go to a course with a homework draft
    # AND: Click on the homework draft
    # AND: Change all the required fields
    # AND: Click on "Cancel"

    # THEN: User is taken back to the Calender
    # AND: The edits should not be saved


@expected_failure
@test_case('')
@tutor
def test_delete_an_opened_homework(tutor_base_url, selenium, teacher):
    """Delete an opened homework."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course with an opened homework

    # WHEN: Go to a course with open homework
    # AND: Click on an opened homework
    # AND: Click "Delete"
    # AND: Click "Yes"

    # THEN: User is taken back to the Calender
    # AND: The homework should no longer be on the calender


@expected_failure
@test_case('')
@tutor
def test_delete_an_unopened_homework(tutor_base_url, selenium, teacher):
    """Delete an unopened homework."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course with an unopened homework

    # WHEN: Go to a course with unopened homework
    # AND: Click on an unopened homework
    # AND: Click "Delete"
    # AND: Click "Yes"

    # THEN: User is taken back to the Calender
    # AND: The homework should no longer be on the calender


@expected_failure
@test_case('')
@tutor
def test_delete_a_homework_draft(tutor_base_url, selenium, teacher):
    """Delete an homework draft."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course with a homework draft

    # WHEN: Go to a course with homework draft
    # AND: Click on the homework draft
    # AND: Click "Delete"
    # AND: Click "Yes"

    # THEN: User is taken back to the Calender
    # AND: The homework draft should no longer be on the calender


@expected_failure
@test_case('')
@tutor
def test_edit_a_homework_draft(tutor_base_url, selenium, teacher):
    """Edit a homework draft."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course with a draft homework

    # WHEN: Click on a homework draft
    # AND: Change all the required fields
    # AND: Click "publish"

    # THEN: User is taken back to the Calender
    # AND: Edited draft with all info changed is published


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_see_what_students_see_button(tutor_base_url, selenium, teacher):
    """Test visibility of 'see what student can see' button."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course with a reading or homework

    # WHEN: click on the reading or homework
    # AND: Click "edit"

    # THEN: The "see what student can see" button should be visible"


@expected_failure
@test_case('')
@tutor
def test_publish_an_external_assignment(tutor_base_url, selenium, teacher):
    """Publish an external assignment."""
    # GIVEN: Logged into Tutor as a teacher

    # WHEN: click a date on the dashboard, then click "add external assignment"
    # AND: fill in all the required fields
    # AND: click "Publish"

    # THEN: User is taken back to the Calender
    # AND: A new reading assignment should be visible on calender


@expected_failure
@test_case('')
@tutor
def test_save_external_assignment_as_draft(tutor_base_url, selenium, teacher):
    """Save an external assignment draft."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click a date on the dashboard, then click "add external assignment"
    # AND: Fill in all the required fields
    # AND: Click “save as draft

    # THEN: User is taken back to the Calender
    # AND: A new reading draft should be visible on calender


@expected_failure
@test_case('')
@tutor
def test_edit_an_external_assignment(tutor_base_url, selenium, teacher):
    """Edit an external assignment."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course with an external assignment

    # WHEN: Go to course with an external assignment
    # AND: Click on the external assignment
    # AND: Change all the required fields
    # AND: Click "publish"

    # THEN: User is taken back to the Calender
    # AND: An edited external assignment is visible on calendar


@expected_failure
@test_case('')
@tutor
def test_edit_an_external_draft(tutor_base_url, selenium, teacher):
    """Edit an external assignment draft."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course with a draft external assignment

    # WHEN: Click on an external assignment draft
    # AND: Change all the required fields
    # AND: Click "publish"

    # THEN: User is taken back to the Calender
    # AND: Edited draft is published


@expected_failure
@test_case('')
@tutor
def test_delete_an_external_assignment(tutor_base_url, selenium, teacher):
    """Delete an external assignment."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course with an external assignment

    # WHEN: Go to the course with external assignment
    # AND: Click on an external assignment
    # AND: Click “delete"

    # THEN: User is taken back to the Calender
    # AND: The external assignment is no longer visible on the calendar"


@expected_failure
@test_case('')
@tutor
def test_delete_an_external_draft(tutor_base_url, selenium, teacher):
    """Delete an external assignment draft."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course with a draft external assignment

    # WHEN: Click on an external assignment draft
    # AND: Click "delete"
    # AND: Click "yes"

    # THEN: User is taken back to the Calender
    # AND: The draft is deleted and no longer visible on the calendar


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_cancel_edit_external_assignment(tutor_base_url, selenium, teacher):
    """Cancel editing an external assignment."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course with an external assignment

    # WHEN: Click on an external assignment.
    # AND: Change all the required fields
    # AND: Click “cancel"

    # THEN: User is taken back to the Calender
    # AND: No changes should be made on the assignment


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_cancel_edit_an_external_draft(tutor_base_url, selenium, teacher):
    """Cancel editing an external assignment draft."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course with an external assignment draft

    # WHEN: Click on an external assignment draft
    # AND: Change all the required fields
    # AND: Click “cancel"

    # THEN: User is taken back to the Calender
    # AND: No changes should be made on the draft


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_add_external_assignment_with_empty_fields(tutor_base_url, selenium,
                                                   teacher):
    """Cancel editing an external assignment."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click on an external assignment
    # AND: Change some of the required fields and leave some blank
    # AND: Click "Publish"

    # THEN: Red outlines should popup for required fields


@expected_failure
@test_case('')
@tutor
def test_add_a_new_event(tutor_base_url, selenium, teacher):
    """Add a new event."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Go to the course page
    # AND: Click on a date on the dashboard
    # AND: Click "add event"
    # AND: Fill in all the required fields
    # AND: click "Publish"

    # THEN: User is taken back to the Calender
    # AND: A new event should be visible on the calendar


@expected_failure
@test_case('')
@tutor
def test_save_an_event_draft(tutor_base_url, selenium, teacher):
    """Saving a draft event."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: click on a date on the dashboard, then click "add event"
    # AND: fill in all the required fields
    # AND: click "Save as Draft"

    # THEN: User is taken back to the Calender
    # AND: A new event draft should be visible on the calendar


@expected_failure
@test_case('')
@tutor
def test_edit_a_published_event(tutor_base_url, selenium, teacher):
    """Edit a published event."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course
    # AND: Has an published event

    # WHEN: Click on a published event
    # AND: Change all the required fields
    # AND: Click "Publish"

    # THEN: User is taken back to the Calender
    # AND: The event should be visible on the calendar with its info updated"


@expected_failure
@test_case('')
@tutor
def test_edit_an_event_draft(tutor_base_url, selenium, teacher):
    """Edit an draft event."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course
    # AND: Has an draft event

    # WHEN: Click on  event draft
    # AND: Change all the required fields
    # AND: Click "Publish"

    # THEN: User is taken back to the Calender
    # AND: The event draft should be visible on the calendar with updated info


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_cancel_edit_a_draft(tutor_base_url, selenium, teacher):
    """Cancel editing a draft event."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course
    # AND: Has an draft event

    # WHEN: Click on  event draft
    # AND: Change all the required fields
    # AND: Click "Cancel"

    # THEN: User is taken back to the Calender
    # AND: No changes should be made on the draft


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_cancel_edit_a_published_event(tutor_base_url, selenium, teacher):
    """Cancel editing a published event."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course
    # AND: Has an published event

    # WHEN: Click on  published event
    # AND: Change all the required fields
    # AND: Click "Cancel"

    # THEN: User is taken back to the Calender
    # AND: No changes should be made on the event


@expected_failure
@test_case('')
@tutor
def test_delete_a_published_event(tutor_base_url, selenium, teacher):
    """Delete a published event."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course
    # AND: Has an published event

    # WHEN: Click on  published event
    # AND: Click "Delete"

    # THEN: User is taken back to the Calender
    # AND: The deleted event should no longer be visible


@expected_failure
@test_case('')
@tutor
def test_delete_an_event_draft(tutor_base_url, selenium, teacher):
    """Delete a draft event."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course
    # AND: Has an draft event

    # WHEN: Click on draft event
    # AND: Click "Delete"

    # THEN: User is taken back to the Calender
    # AND: The deleted event draft should no longer be visible
