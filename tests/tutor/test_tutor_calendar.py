"""Test the Tutor teacher course calendar functions."""

from tests.markers import expected_failure, nondestructive, test_case, tutor


@expected_failure
@test_case('')
@nondestructive
@tutor
def test_view_the_instructor_calendar(tutor_base_url, selenium, teacher):
    """Test teacher to view the calendar."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN: Select a Tutor course

    # THEN: The teacher is presented their calendar dashboard


@expected_failure
@test_case('')
@nondestructive
@tutor
def test_view_student_scores_with_the_calendar_button(
        tutor_base_url, selenium, teacher):
    """Test teacher to view student score with calendar button."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN: Select a Tutor course
    # AND: Click "Student Scores"

    # THEN: the teacher is presented with their students' scores
    # each section/period


@expected_failure
@test_case('')
@tutor
def test_edit_an_unopened_homework(tutor_base_url, selenium, teacher):
    """Edit an unopened homework."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Go to a course with unopened homework
    # AND: Click on an unopened homework
    # AND: Change all the required fields
    # AND: Click "publish"

    # THEN: User is taken back to the Calender
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
@test_case('')
@nondestructive
@tutor
def test_view_performance_forecast_using_the_calendar_button(
        tutor_base_url, selenium, teacher):
    """Test teacher to view performance forecast with calendar button."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN: Select a Tutor course
    # AND: Click "Performance Forecast"

    # THEN: the teacher is presented with performance forecast fot the sections


@expected_failure
@test_case('')
@nondestructive
@tutor
def test_cancel_editing_homework(tutor_base_url, selenium, teacher):
    """Cancel editing a published homework."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at a course with published homework

    # WHEN: Click on edit an published homework
    # AND: Change all the required fields
    # AND: Click "Cancel"

    # THEN: User is taken back to the Calender
    # AND: The edits should not be saved


@expected_failure
@test_case('')
@nondestructive
@tutor
def test_view_a_reading_assignment_summary(tutor_base_url, selenium, teacher):
    """Test teacher to view a reading assignment summary."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course
    # AND: has a reading assignment

    # WHEN: Select a Tutor course
    # AND: From the user calendar, click on a reading that is displayed

    # THEN: the teacher is presented with a summary of information about
    # the reading


@expected_failure
@test_case('')
@nondestructive
@tutor
def test_view_a_homework_assignment_summary(tutor_base_url, selenium, teacher):
    """Test teacher to view a homework assignment ."""
    # GIVEN: A logged in teacher user
    # AND: has a homework assignment

    # WHEN: Select a Tutor course
    # AND: From the user calendar, click on a homework assignment
    # that is displayed"

    # THEN: The teacher is presented with a summary of the homework assignment.


@expected_failure
@test_case('')
@nondestructive
@tutor
def test_view_an_external_assignment_summary(
        tutor_base_url, selenium, teacher):
    """Test teacher to view an external assignment."""
    # GIVEN: A logged in teacher user
    # AND: has an external assignment

    # WHEN: Select a Tutor course
    # AND: From the user calendar, click on external assignment
    # that is displayed""

    # THEN: The teacher is presented with a summary of the external
    # assignment.


@expected_failure
@test_case('')
@nondestructive
@tutor
def test_view_an_event_summary(tutor_base_url, selenium, teacher):
    """Test teacher to view an event."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course
    # AND: has a event

    # WHEN:  Select a Tutor course
    # AND: From the user calendar, click on an event that is displayed""

    # THEN: The teacher is presented with a summary of the selected event.


@expected_failure
@test_case('')
@nondestructive
@tutor
def test_open_the_reference_book_with_the_calendar_button(
        tutor_base_url, selenium, teacher):
    """Test teacher to open a reference book with calendar button."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN: Select a Tutor course
    # AND: Click on the 'Browse The Book' button on the user dashboard""

    # THEN: The teacher is presented with the book in a new tab


@expected_failure
@test_case('')
@nondestructive
@tutor
def test_cancel_editing_a_draft_homework(tutor_base_url, selenium, teacher):
    """Cancel editing a published homework draft."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at a course with an existing homework draft

    # WHEN: Click on edit the homework draft
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
    # AND: User is at a course with an opened homework

    # WHEN: Click on an opened homework
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
    # AND: User is at a course with an unopened homework

    # WHEN: Click on an unopened homework
    # AND: Click "Delete"
    # AND: Click "Yes"

    # THEN: User is taken back to the Calender
    # AND: The homework should no longer be on the calender


@expected_failure
@test_case('')
@tutor
def test_delete_a_draft_homework(tutor_base_url, selenium, teacher):
    """Delete an homework draft."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at a course with a homework draft

    # WHEN: Go to a course with homework draft
    # AND: Click on the homework draft
    # AND: Click "Delete"
    # AND: Click "Yes"

    # THEN: User is taken back to the Calender
    # AND: The homework draft should no longer be on the calender


@expected_failure
@test_case('')
@tutor
def test_edit_a_draft_homework(tutor_base_url, selenium, teacher):
    """Edit a homework draft."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at a course with a homework draft

    # WHEN: Click on edit a homework draft
    # AND: Change all the required fields
    # AND: Click "publish"

    # THEN: User is taken back to the Calender
    # AND: Edited draft with all info changed is published


@expected_failure
@test_case('')
@nondestructive
@tutor
def test_return_to_the_course_picker(tutor_base_url, selenium, teacher):
    """Test teacher return to course picker by clicking logo."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN: Select a Tutor course
    # AND: Click on the OpenStax logo at the top of the page""

    # THEN: The teacher should be returned to a page displaying
    # all of their courses.


@expected_failure
@test_case('')
@nondestructive
@tutor
def test_add_assignments_by_drag_and_drop(tutor_base_url, selenium, teacher):
    """Test teacher to add assignments/readings/events by drag and drop."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN: Select a Tutor course
    # AND: Drag ""assignments/reading/external assignment/event""
    # from the left menu to a day on calendar""

    # THEN: The page for creating new assignment/reading/external
    # assignment/event should open with the due date already fill in as
    # the day user dragged it to on calendar.


@expected_failure
@test_case('')
@nondestructive
@tutor
def test_add_assignment_to_past_day(tutor_base_url, selenium, teacher):
    """Test teacher to attempt to add and assignment to past day."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN: Select a Tutor course
    # AND: Click on a past day and drag assignments onto a past day""

    # THEN: User shouldn't be able to access past dates on calendar


@expected_failure
@test_case('')
@nondestructive
@tutor
def test_question_library_loads(tutor_base_url, selenium, teacher):
    """Test if question library works under teacher."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN:  Select a Tutor course
    # AND: Click question library from the calendar"

    # THEN: user should be taken to the question library


@expected_failure
@test_case('')
@nondestructive
@tutor
def test_view_instructor_training_wheels_for_the_dashboard(
        tutor_base_url, selenium, teacher):
    """Test teacher to use training wheels for dashboard`."""
    # GIVEN: A logged in teacher user

    # WHEN: Click on a current course to navigate to Dashboard
    # AND: Activate Spy Mode
    # AND: Pop-up should show with the options
    # ""View Tips Now"" and ""View Later""
    # AND:Click ""View Tips Now""

    # THEN: User should be taken through a training wheels tour
    # detailing the creation of assignments,
    # the options at the top, the user dropdown options, and the navbar


@expected_failure
@test_case('')
@nondestructive
@tutor
def test_see_what_students_see_button(tutor_base_url, selenium, teacher):
    """Test visibility of 'see what student can see' button."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at a course with a reading or homework

    # WHEN: click on the reading or homework
    # AND: Click "Edit"

    # THEN: The "see what student can see" button should be visible


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
    # AND: User is at a course with an external assignment

    # WHEN: Click on edit the external assignment
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
    # AND: User is at a course with an draft external assignment

    # WHEN: Click on edit an external assignment draft
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
    # AND: User is at a course with an external assignment

    # WHEN: Click on an external assignment
    # AND: Click "delete"
    # AND: Click "yes"

    # THEN: User is taken back to the Calender
    # AND: The external assignment is no longer visible on the calendar


@expected_failure
@test_case('')
@tutor
def test_delete_an_external_draft(tutor_base_url, selenium, teacher):
    """Delete an external assignment draft."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at a course with a draft external assignment

    # WHEN: Click on an external assignment draft
    # AND: Click "delete"
    # AND: Click "yes"

    # THEN: User is taken back to the Calender
    # AND: The draft is deleted and no longer visible on the calendar


@expected_failure
@test_case('')
@nondestructive
@tutor
def test_term_appearance_new(tutor_base_url, selenium, teacher):
    """Test terms/PP appearance for onboarding | new instructor."""
    # GIVEN:  Be at the Tutor page

    # WHEN: Log into verified teacher account
    # AND: Pick a course

    # THEN: In that course, the instructor is shown terms
    # AND:Once agreed, the instructor is taken to the course dashboard.


@expected_failure
@test_case('')
@nondestructive
@tutor
def test_cancel_edit_external_assignment(tutor_base_url, selenium, teacher):
    """Cancel editing an external assignment."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at a course with an external assignment

    # WHEN: Click on an external assignment.
    # AND: Change all the required fields
    # AND: Click "cancel"

    # THEN: User is taken back to the Calender
    # AND: No changes should be made on the assignment


@expected_failure
@test_case('')
@nondestructive
@tutor
def test_term_appearance_exist(tutor_base_url, selenium, teacher):
    """Test terms/PP appearance for onboarding | existing instructor."""
    # GIVEN: Having changed the terms of a particular course as admin

    # WHEN: Log in as teacher and go to that course page.
    # AND: Enters a course.

    # THEN: the teacher is shown the terms when they changed.


@expected_failure
@test_case('')
@nondestructive
@tutor
def test_cancel_editing_an_external_draft(tutor_base_url, selenium, teacher):
    """Cancel editing an external assignment draft."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at a course with an external assignment draft

    # WHEN: Click on edit an external assignment draft
    # AND: Change all the required fields
    # AND: Click "Cancel"

    # THEN: User is taken back to the Calender
    # AND: No changes should be made on the draft


@expected_failure
@test_case('')
@nondestructive
@tutor
def test_physics_student_preview_videos(tutor_base_url, selenium, teacher):
    """Test teacher to embed physics student preview videos."""
    # GIVEN: A logged in teacher user

    # WHEN: Navigate to a Physics class
    # AND: Click on the small video icon on the top navbar

    # Dashboard preview: https://usertu.be/IbYU5py9YP8
    # Physics HW: https://usertu.be/Ic2_9LYXY84
    # Physics Reading: https://usertu.be/tCocd4jCVCA


@expected_failure
@test_case('')
@nondestructive
@tutor
def test_add_external_assignment_with_empty_fields(
        tutor_base_url, selenium, teacher):
    """Cancel editing an external assignment."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at a course with an external assignment

    # WHEN: Click on edit an external assignment
    # AND: Change some of the required fields and leave some blank
    # AND: Click "Publish"

    # THEN: Red outlines should popup for required fields


@expected_failure
@test_case('')
@tutor
def test_add_a_new_event(tutor_base_url, selenium, teacher):
    """Add a new event."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at a course calendar

    # WHEN: Click on a date on the dashboard
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

    # WHEN: click on a date on the dashboard
    # AND: click "add event"
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
    # AND: User is at a course with a published event

    # WHEN: Click on edit a published event
    # AND: Change all the required fields
    # AND: Click "Publish"

    # THEN: User is taken back to the Calender
    # AND: The event should be visible on the calendar with its info updated


@expected_failure
@test_case('')
@tutor
def test_edit_an_event_draft(tutor_base_url, selenium, teacher):
    """Edit an draft event."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at a course with a draft event

    # WHEN: Click on edit event draft
    # AND: Change all the required fields
    # AND: Click "Publish"

    # THEN: User is taken back to the Calender
    # AND: The event draft should be visible on the calendar with updated info


@expected_failure
@test_case('')
@nondestructive
@tutor
def test_sociology_student_preview_videos(tutor_base_url, selenium, teacher):
    """Test teacher to embed sociology student preview videos."""
    # GIVEN: A logged in teacher user

    # WHEN:  Navigate to a Sociology class
    # AND: Click on the small video icon on the top navbar

    # THEN: User is taken to usertube videos with the following links:
    # Dashboard preview: https://usertu.be/IbYU5py9YP8
    # Soci HW: https://usertu.be/Ki-y2AywXlI
    # Soci Reading: https://usertu.be/GF05th84Bw8


@expected_failure
@test_case('')
@nondestructive
@tutor
def test_cancel_edit_a_draft(tutor_base_url, selenium, teacher):
    """Cancel editing a draft event."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at a course with a draft event

    # WHEN: Click on edit event draft
    # AND: Change all the required fields
    # AND: Click "Cancel"

    # THEN: User is taken back to the Calender
    # AND: No changes should be made on the draft


@expected_failure
@test_case('')
@nondestructive
@tutor
def test_biology_student_preview_videos(tutor_base_url, selenium, teacher):
    """Test teacher to embed biology student preview videos."""
    # GIVEN: A logged in teacher user

    # WHEN: Navigate to a Biology class
    # AND: Click on the small video icon on the top navbar

    # THEN: User is taken to usertube videos embedded with the following links:
    # Dashboard preview: https://usertu.be/IbYU5py9YP8
    # Bio HW: https://usertu.be/kzvHLFsQDTM
    # Bio Reading: https://usertu.be/4neNaHRyTUw


@expected_failure
@test_case('')
@tutor
def test_cancel_edit_a_published_event(tutor_base_url, selenium, teacher):
    """Cancel editing a published event."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at a course with a published event

    # WHEN: Click on published event
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
    # AND: User is at a course with a published event

    # WHEN: Click on published event
    # AND: Click "Delete"
    # AND: Click "yes"

    # THEN: User is taken back to the Calender
    # AND: The deleted event should no longer be visible


@expected_failure
@test_case('')
@tutor
def test_delete_an_event_draft(tutor_base_url, selenium, teacher):
    """Delete a draft event."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at a course with a draft event

    # WHEN: Click on draft event
    # AND: Click "Delete"
    # AND: Click "yes"

    # THEN: User is taken back to the Calender
    # AND: The deleted event draft should no longer be visible
