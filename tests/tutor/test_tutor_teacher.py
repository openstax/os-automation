"""Test the Tutor teacher functions."""

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


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_view_student_scores(tutor_base_url, selenium, teacher):
    """View student scores."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click on the "Student Scores" button
    # AND: Click on the tab for the desired period

    # THEN: Scores for selected period are displayed in a table


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_section_tab(tutor_base_url, selenium, teacher):
    """Switch to view different sections of student scores."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course with more than one sections

    # WHEN: Click on the "Student Scores" button

    # THEN: Period tabs should be displayed


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_switch_between_score_representation(
        tutor_base_url, selenium, teacher):
    """Switch to view different representations of scores."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click on a course
    # AND: Go to student scores
    # AND: switch between "display as: %/#"

    # THEN: The representation of score representation change accordingly


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_download_spreadsheet_of_class_score(
        tutor_base_url, selenium, teacher):
    """Download class scores as a spreadsheet."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click on a course
    # AND: Click on the "Student Scores" button
    # AND: Click on the "Export" button
    # AND: Select destination for saved spreadsheet in the pop up
    # AND: Click on the "Save" Button on the pop up

    # THEN: Spreadsheet of scores is saved as an xlsx file


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_view_performance_forecast_for_single_student(tutor_base_url, selenium,
                                                      teacher):
    """View performance forecast for a single student from score page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click on a course
    # AND: Click on the "Student Scores" button
    # AND: Click on the name of selected student

    # THEN: Performance Forecast for selected student is displayed


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_sort_the_student_list_by_last_name(tutor_base_url, selenium, teacher):
    """Sort student by last name in the score page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course
    # AND: Has at least two students

    # WHEN: Click on a course
    # AND: Click on the "Student Scores" button
    # AND: Click on "Name and Student ID" on the table
    # AND: Click on "Name and Student ID" on the table again

    # THEN: The students are sorted alphabetically by last name.


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_sort_score_by_assignment_completion(tutor_base_url, selenium,
                                             teacher):
    """Sort student by completion of an assignment in the score page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course
    # AND: Has at least two students
    # AND: Students has somewhat finished an assignment

    # WHEN: If the user has more than one course, click on a Tutor course name
    # AND: Click on the "Student Scores" button
    # AND: Click "Progress"

    # THEN: Students are sorted by completion of selected assignment.


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_sort_score_by_assignment_score(tutor_base_url, selenium, teacher):
    """Sort student by scores of an assignment in the score page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course
    # AND: Has at least two students
    # AND: Has a graded assignment

    # WHEN: If the user has more than one course, click on a Tutor course name
    # AND: Click on the "Student Scores" button
    # AND: Click "Score"

    # THEN: Students are sorted by completion of selected assignment.


@expected_failure
@test_case('')
@tutor
def test_edit_score_weights(tutor_base_url, selenium, teacher):
    """Edit score weights."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: If the user has more than one course, click on a Tutor course name
    # AND: Click on the "Student Scores" button
    # AND: Click "set weights" on the page

    # THEN: A window for edit weights should pop up
    # AND: user should be able to change the weights from this window


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_cancel_edit_score_weights(tutor_base_url, selenium, teacher):
    """Cancel editing score weights."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: If the user has more than one course, click on a Tutor course name
    # AND: Click on the "Student Scores" button
    # AND: Click "set weights" on the page
    # AND. click "set weights" on the page
    # AND.  change some weights in the popup window
    # AND. click cancel button

    # THEN: User is taken back to the scores page, nothing should change


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_click_see_why_in_score_weights(tutor_base_url, selenium, teacher):
    """Go to 'see why' blog page from score weights."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: If the user has more than one course, click on a Tutor course name
    # AND: Click on the "Student Scores" button
    # AND: click "set weights" at student scores page
    # AND: click "see why" from the set weights page

    # THEN: the openstax blog should open up in another tab"


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_scrolling_in_assignments_section(tutor_base_url, selenium, teacher):
    """Scroll left and right in assignment section in score page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click on the "Student Scores" button
    # AND: Scroll left or right in the table of scores for view assignments

    # THEN: Table should move accordingly with the scrolling"


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_score_page_for_section_with_no_scores(tutor_base_url, selenium,
                                               teacher):
    """Test messages for no score sections in score page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course
    # AND: The class has no student or no assignment

    # WHEN: Click on the "Student Scores" button

    # THEN: The page contains button to settings and roaster"


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_view_overall_students_performance(tutor_base_url, selenium, teacher):
    """View the overall performance of students in scores page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course
    # AND: Has finished assignment

    # WHEN:  Click on the "Student Scores" button
    # AND: Click on the tab for the chosen period
    # AND: Click on the "Review" button under the selected reading or homework.

    # THEN: Each question has a correct response displayed"


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_view_student_assignment_detail(tutor_base_url, selenium, teacher):
    """View student's assignment from score page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course
    # AND: Has finished assignment

    # WHEN:  Click on the "Student Scores" button
    # AND: click a student's score for a specific assignment

    # THEN: the teacher is taken to the assignment page with student's answers


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_no_score_is_displayed_for_readings(tutor_base_url, selenium, teacher):
    """Check no score for readings in the score page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course
    # AND: Has finished reading

    # WHEN:  Click on the "Student Scores" button
    # AND: Scroll to a reading assignment

    # THEN: The user is presented with progress icon but no score for reading


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_scores_info_icon(tutor_base_url, selenium, teacher):
    """Check the info icon in the score page displays proper information."""
    # GIVEN: Logged into Tutor as a teacher

    # WHEN:  Click on the "Student Scores" button
    # AND:  Click on the info icon next to "Class Performance"

    # THEN: The info icon displays a definition of how class and overall scores
    # are calculated


@expected_failure
@test_case('')
@tutor
def test_accept_late_work(tutor_base_url, selenium, teacher):
    """Accept late work in the score page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course
    # AND: Student has submitted late homework or readings

    # WHEN:  Click on the "Student Scores" button
    # AND: Scroll until an assignment with an orange triangle is found
    # AND: Click on the orange triangle at the upper right  of a progress cell
    # AND: Click "Accept late score" OR "Accept late progress"

    # THEN: The late score replaces the score at due date


@expected_failure
@test_case('')
@tutor
def test_unaccept_late_work(tutor_base_url, selenium, teacher):
    """Unaccept late work in the score page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course
    # AND: Has accepted student's late homework or reading

    # WHEN: Click on the "Student Scores" button
    # AND: Scroll until an assignment with an orange triangle is found
    # AND: Click on the orange triangle at the upper right of a progress cell
    # AND: Click "Use this score" OR "Use this Progress"

    # THEN: The score is converted back to the score at due date"


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_external_assignments_in_the_scores_export(tutor_base_url, selenium,
                                                   teacher):
    """Check that external assignments are not included in exported scores."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course
    # AND: Has given an external assignment

    # WHEN: Click "Student Scores" from user menu
    # AND: Click "Export"

    # THEN: External assignments are not included in the scores export


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_dropped_students_in_student_scores(tutor_base_url, selenium, teacher):
    """Check removal of dropped students in scores page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course
    # AND: Has dropped student(s)

    # WHEN: Click the user menu
    # AND: Click "Student Scores"
    # AND: Click on the period from which user have dropped the student

    # THEN: Dropped student should not be displayed in Student Scores


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_moved_students_in_student_scores(tutor_base_url, selenium, teacher):
    """Check moved students appear in their current sections in scores."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course
    # AND: Has moved a student's period

    # WHEN: Click "Student Scores" from the user menu
    # AND: Click on the period to which the student was moved

    # THEN: The user is presented with the moved student under their new period


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_view_score_at_due_date(tutor_base_url, selenium, teacher):
    """Check teacher view scores at due date in score's page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course
    # AND: Has at least one student
    # AND: Student has finished one assignment

    # WHEN: Click "Student Scores" from the user menu

    # THEN: User is displayed with scores at due date


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_view_current_score(tutor_base_url, selenium, teacher):
    """View current score in score's page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course
    # AND: Has given an assignment

    # WHEN: Click "Student Scores" from the calendar dashboard
    # AND: Click on the orange flag in the upper right corner of a progress
    # cell for the desired student

    # THEN: The user is presented with current score


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_view_period_performance_forecast(tutor_base_url, selenium, teacher):
    """View performance forecast page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click on "Performance Forecast" in the user menu
    # AND: Click on the desired period

    # THEN: The period Performance Forecast is presented to the user


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_performance_forecast_info_icon(tutor_base_url, selenium, teacher):
    """View info icon in performance forecast page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click on "Performance Forecast" in the user menu
    # AND: Hover the cursor over the info icon

    # THEN: Info icon shows an explanation of the data


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_view_the_performance_color_key(tutor_base_url, selenium, teacher):
    """View performance color key in performance forecast page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click on "Performance Forecast" in the user menu

    # THEN: The performance color key is presented to the user


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_period_tabs_are_shown(tutor_base_url, selenium, teacher):
    """Check period tabs in performance forecast page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course
    # AND: Has more than one period

    # WHEN: Click on "Performance Forecast" in the user menu

    # THEN: The period tabs are shown to the user


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_period_with_zero_answers(tutor_base_url, selenium, teacher):
    """Check that a period with no answers doesn't show section breakdowns."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course
    # AND: Has a period that hasn't answered assignments

    # WHEN: Click on "Performance Forecast" in the user menu
    # AND: Click on the period with zero answers

    # THEN: The user should see no section breakdowns and the message:
    # "There have been no questions worked for this period."


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_perforemance_forecast_weaker_areas(tutor_base_url, selenium, teacher):
    """Check weaker areas show up to four problematic sections."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click on "Performance Forecast" in the user menu
    # AND: Click on the desired period

    # THEN: Weaker Areas show up to four problematic sections


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_review_all_questions(tutor_base_url, selenium, teacher):
    """View questions in question library."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click "Question Library" from the user menu
    # AND: Select a section or chapter
    # AND: Click "Show Questions"

    # THEN: The user is presented with all the questions for the chapter


@expected_failure
@test_case('')
@tutor
def test_exclude_certain_questions(tutor_base_url, selenium, teacher):
    """Exclude certain questions in question library."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click "Question Library" from the user menu
    # AND: Select a section or chapter
    # AND: Click "Show Questions"
    # AND: Hover over the desired question and click "Exclude question"

    # THEN: Question is excluded


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_switch_between_reading_and_homework_questions(
        tutor_base_url, selenium, teacher):
    """Switch to view reading and homework questions in question library."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click "Question Library" from the user menu
    # AND: Select a section or chapter
    # AND: Click "Show Questions"
    # AND: Click on the "Reading" tab

    # THEN: Exercises that are only for Reading appear


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_question_library_pinned_tab(tutor_base_url, selenium, teacher):
    """Check the pinned tab to the top of the screen in question library."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click "Question Library" from the user menu
    # AND: Select a section or chapter
    # AND: Click "Show Questions"
    # AND: Scroll down

    # THEN: Tabs are pinned to the top of the screen when scrolled


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_browse_corresponding_chapter_in_the_book(tutor_base_url, selenium,
                                                  teacher):
    """Browse questions of a certain chapter in question library."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click "menu"
    # AND: Click "question library"
    # AND: Click "browse this chapter"

    # THEN: content of the chapter user choose is displayed


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_section_in_question_library(tutor_base_url, selenium, teacher):
    """Jump between chapters with breadcrumbs in question library."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click "menu"
    # AND: Click "question library"
    # AND: Choose a section besides the intro chapter
    # AND: Choose sections from top left side of page

    # THEN: When a subchapter number is clicked on, the book shows the content
    # of the subchapter user've chosen"


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_go_to_question_details(tutor_base_url, selenium, teacher):
    """Go to question details page in question library."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click "menu"
    # AND: Click "question library"
    # AND: Click on a chapter besides intro
    # AND: Click "question details"

    # THEN: Question details page are shown


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_report_errata_about_questions(tutor_base_url, selenium, teacher):
    """Report a errata for a question in question library."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click "Question Library" from the user menu
    # AND: Select a section or chapter
    # AND: Click "Show Questions"
    # AND: Hover over the desired question and click "Question details"
    # AND: Click "Report an error"

    # THEN: A new tab with the assessment errata form appears
    # AND: The assessment ID is already filled in


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_preview_feedback(tutor_base_url, selenium, teacher):
    """Preview feedback for a question in question library."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click "menu"
    # AND: Click "question library"
    # AND: Click on a chapter besides intro
    # AND: Click "question details"
    # AND: Click "preview feedback"

    # THEN: Feedback of the question is shown"


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_switch_between_questions(tutor_base_url, selenium, teacher):
    """Switch between questions using arrows in question library."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click "menu"
    # AND: Click "question library"
    # AND: Click on a chapter besides intro
    # AND: Click "question details"
    # AND: Click the right arrow

    # THEN: User should be navigated to the next question


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_go_to_card_view(tutor_base_url, selenium, teacher):
    """Switch to card view in question library."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click "menu"
    # AND: Click "question library"
    # AND: Click on a chapter besides intro
    # AND: Click "question details"
    # AND: Click "back to card view"

    # THEN: The questions now displays in card view


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_errata_with_empty_fields(tutor_base_url, selenium, teacher):
    """Attempt to suggest a correction without filling in required fields."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click "menu"
    # AND: Click "question library"
    # AND: Click on a chapter besides intro
    # AND: Click "question details"
    # AND: Click "suggest an error"
    # AND: Do not fill out the required fields, click "submit"

    # THEN: Could not submit the form
    # AND: User is prompted to fill out the required field


@expected_failure
@test_case('')
@tutor
def test_exclude_a_question(tutor_base_url, selenium, teacher):
    """Exclude a question in question details in question library."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click "menu"
    # AND: Click "question library"
    # AND: Click on a chapter besides intro
    # AND: Click "question details"
    # AND: Click "exclude question"

    # THEN: The chosen question is excluded


@expected_failure
@test_case('')
@tutor
def test_create_a_new_course(tutor_base_url, selenium, teacher):
    """Create a new course."""
    # GIVEN: Logged into Tutor as a teacher

    # WHEN: From menu, click "create a course"
    # AND: Fill out the form

    # THEN: A new course is created
    # AND: User is taken to the course dashboard


@expected_failure
@test_case('')
@tutor
def test_copy_a_course_from_past_courses(tutor_base_url, selenium, teacher):
    """Copy a new course from a existing course."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Choose a course user want to copy, click "copy this course"
    # AND: Fill out the form

    # THEN: A new course is created
    # AND: User is taken to the course dashboard, old assignments are present


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_cancel_creating_a_new_course(tutor_base_url, selenium, teacher):
    """Cancel creating a new course."""
    # GIVEN: Logged into Tutor as a teacher

    # WHEN: From menu, click "create a course"
    # AND: Fill out the form
    # AND: Click "cancel"

    # THEN: User is taken back to course picker
    # AND: No course is created


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_cancel_copying_a_new_course(tutor_base_url, selenium, teacher):
    """Cancel copying a new course."""
    # GIVEN: Logged into Tutor as a teacher

    # WHEN: Choose a course user want to copy, then click "copy this course"
    # AND: Fill out the form
    # AND: Click "cancel"

    # THEN: User is taken back to course picker
    # AND: No course is created


@expected_failure
@test_case('')
@tutor
def test_create_new_course_with_empty_fields(
        tutor_base_url, selenium, teacher):
    """Attempt to create a new course without filling in required fields."""
    # GIVEN: Logged into Tutor as a teacher

    # WHEN: From menu, click "create a course"
    # AND: Fill out the form, leaving some of the fields blank

    # THEN: Course could not be created
    # AND: User is prompted to fill out the required fields


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_copy_course_with_empty_fields(tutor_base_url, selenium, teacher):
    """Attempt to copy a course without filling in required fields."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Choose a course user want to copy, click "copy this course"
    # AND: Fill out the form, leaving some of the fields blank

    # THEN: Course could not be created
    # AND: User is prompted to fill in the required fields


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_copy_course_with_old_version_textbook(tutor_base_url, selenium,
                                               teacher):
    """Attempt to copy a course with old version textbook should fail."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course with a old version textbook

    # WHEN: Choose a course with old version textbook, click "copy this course"
    # AND: Fill out the form

    # THEN: Course could not be created
    # AND: User should see massage: "the textbook is too old to be supported."


@expected_failure
@test_case('')
@tutor
def test_change_course_name(tutor_base_url, selenium, teacher):
    """Change course name in course setting."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Select a Tutor course
    # AND: Go to "Course Setting"
    # AND: Click the pencil icon next to course name

    # THEN: a popup window for edit course name should appear
    # AND: user should be able to edit course name


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_switch_between_setting_tabs(tutor_base_url, selenium, teacher):
    """Switch between tabs in course setting."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Select a Tutor course
    # AND: Go to "Course Setting"
    # AND: Switch between "student access" and "dates and time" tabs

    # THEN: the content of the page should change accordingly


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_student_enrollment_url(tutor_base_url, selenium, teacher):
    """View student enrollment url for different sections."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Select a Tutor course
    # AND: Go to "Course Setting"

    # THEN: Student enrollment url for different sections should be present


@expected_failure
@test_case('')
@tutor
def test_change_course_time_zone(tutor_base_url, selenium, teacher):
    """Change course time zone in course settings."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Select a Tutor course
    # AND: Go to "Course Setting"
    # AND: Click the "dates and time" tab
    # AND: Click the pencil icon next to time zone

    # THEN: A popup window for changing the time zone should appear
    # AND: User should be able to change time zone in the popup window


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_cancel_changing_course_name(tutor_base_url, selenium, teacher):
    """Cancel changing course name in course settings."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Select a Tutor course
    # AND: Go to "Course Setting"
    # AND: Clicking the pencil icon next to course name
    # AND: Change the course name in the popup window
    # AND: Click x

    # THEN: Course name shouldn't change


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_cancel_changing_course_time_zone(tutor_base_url, selenium, teacher):
    """Cancel changing course time zone in course settings."""
    # GIVEN:  Logged into tutor as a teacher
    # AND: has an existing course

    # WHEN: Select a course
    # AND: Click "dates and time"
    # AND: Click the pencil icon
    # AND: Change time zone selection
    # AND: Click x

    # THEN: Course time zone shouldn't change


@expected_failure
@test_case('')
@tutor
def test_add_a_new_section(tutor_base_url, selenium, teacher):
    """Add a new section in course roster."""
    # GIVEN: Logged into tutor as a teacher
    # AND: has a existing course

    # WHEN: Select a course
    # AND: click "course roster"
    # AND: Click "add a section"
    # AND: Enter a section name, click enter

    # THEN: A new section should appear


@expected_failure
@test_case('')
@tutor
def test_add_a_new_instructor(tutor_base_url, selenium, teacher):
    """Add a new instruction in course roster."""
    # GIVEN: Logged into tutor as a teacher
    # AND: has a existing course

    # WHEN: Select a Tutor course
    # AND: Click "course roster"
    # AND: Click "add a new instructor"
    # AND: Add instructor name, click enter

    # THEN: A url link that instructor could use to join this course is shown


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_roster_switch_between_sections(tutor_base_url, selenium, teacher):
    """Switch view between sections in course roster."""
    # GIVEN: Logged into tutor as a teacher
    # AND: has a existing course

    # WHEN: Select a Tutor course
    # AND: Click "course roster"
    # AND: Click on another section

    # THEN: user is switched to the other section


@expected_failure
@test_case('')
@tutor
def test_rename_a_section(tutor_base_url, selenium, teacher):
    """Rename a section in course roster."""
    # GIVEN: Logged into tutor as a teacher
    # AND: has a existing course

    # WHEN: Select a Tutor course
    # AND: Click "course roster"
    # AND: Click "rename"
    # AND: Type in new name, click enter

    # THEN: Section is renamed


@expected_failure
@test_case('')
@tutor
def test_delete_a_section(tutor_base_url, selenium, teacher):
    """Delete a section in course roster."""
    # GIVEN: Logged into tutor as a teacher
    # AND: has a existing course with two sections

    # WHEN: Select a Tutor course
    # AND: Click "course roster"
    # AND: Click "delete section"
    # AND: Click "yes"

    # THEN: the section is deleted


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_cancel_delete_a_section(tutor_base_url, selenium, teacher):
    """Cancel deleting a section in course roster."""
    # GIVEN: Logged into tutor as a teacher
    # AND: has a existing course with two sections

    # WHEN:  Select a Tutor course
    # AND: Click "course roster"
    # AND: Click "delete a section"
    # AND: Click "cancel"

    # THEN: The section should not be deleted
