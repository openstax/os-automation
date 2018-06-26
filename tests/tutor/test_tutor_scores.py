"""Tests for Tutor course student scores."""

from tests.markers import expected_failure, nondestructive, test_case, tutor


@test_case('')
@expected_failure
@tutor
def test_score_page(tutor_base_url, selenium, student):
    """Test the score page."""
    # GIVEN:  Logged into Tutor as a student
    # AND: Has enrolled in a class

    # WHEN: The user clicks on score
    # AND: The user clicks on view weight

    # THEN: New weight page pops up and loads


@test_case('')
@expected_failure
@tutor
def test_average_section(tutor_base_url, selenium, student):
    """Test the average section of the homework assignment."""
    # GIVEN:  Logged into Tutor as a student
    # AND: Has enrolled in a class
    # AND: Has a homework assignment

    # WHEN: The user clicks on a homework assignment
    # AND: The user clicks on an answer
    # AND: The user clicks on the arrow next to the average

    # THEN: See the average section widen


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_view_student_scores(tutor_base_url, selenium, teacher):
    """View student scores."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at "student scores" page for a course

    # WHEN: Click on the tab for the desired period

    # THEN: Scores for selected period are displayed in a table


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_section_tab(tutor_base_url, selenium, teacher):
    """Switch to view different sections of student scores."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at a course calendar

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
    # AND: User is at "student scores" page for a course

    # WHEN: Click on the tab "display as: %/#"

    # THEN: The representation of score representation change accordingly


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_download_spreadsheet_of_class_score(
        tutor_base_url, selenium, teacher):
    """Download class scores as a spreadsheet."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at "student scores" page for a course

    # WHEN: Click on the "Export" button
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
    # AND: User is at "student scores" page for a course

    # WHEN: Click on the name of selected student

    # THEN: Performance Forecast for selected student is displayed


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_sort_the_student_list_by_last_name(tutor_base_url, selenium, teacher):
    """Sort student by last name in the score page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at "student scores" page with at least two students

    # WHEN: Click on "Name and Student ID" on the table
    # AND: Click on "Name and Student ID" on the table again

    # THEN: The students are sorted alphabetically by last name


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_sort_score_by_assignment_completion(tutor_base_url, selenium,
                                             teacher):
    """Sort student by completion of an assignment in the score page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at "student scores" page for with at least two students
    # AND: The students have finished some assignments

    # WHEN: Click "Progress"

    # THEN: Students are sorted by completion of selected assignment.


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_sort_score_by_assignment_score(tutor_base_url, selenium, teacher):
    """Sort student by scores of an assignment in the score page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at "student scores" page with at least two students
    # AND: The students have graded assignments

    # WHEN: Click "Score"

    # THEN: Students are sorted by completion of selected assignment.


@expected_failure
@test_case('')
@tutor
def test_edit_score_weights(tutor_base_url, selenium, teacher):
    """Edit score weights."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at "student scores" page for a course

    # WHEN: Click "set weights" on the page

    # THEN: A window for edit weights should pop up
    # AND: user should be able to change the weights from this window


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_cancel_edit_score_weights(tutor_base_url, selenium, teacher):
    """Cancel editing score weights."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at "student scores" page for a course

    # WHEN: Click "set weights" on the page

    # THEN: User is taken back to the scores page, nothing should change


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_click_see_why_in_score_weights(tutor_base_url, selenium, teacher):
    """Go to 'see why' blog page from score weights."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at "student scores" page for a course

    # WHEN: Click "set weights" at student scores page
    # AND: Click "see why" from the set weights page

    # THEN: the openstax blog should open up in another tab


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_scrolling_in_assignments_section(tutor_base_url, selenium, teacher):
    """Scroll left and right in assignment section in score page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at "student scores" page for a course

    # WHEN: Scroll left or right in the table of scores for viewing assignments

    # THEN: Table should move accordingly with the scrolling


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_score_page_for_section_with_no_scores(tutor_base_url, selenium,
                                               teacher):
    """Test messages for no score sections in score page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: The user has a class with no student or no assignment

    # WHEN: Click on the "Student Scores" button

    # THEN: The page contains button to settings and roaster


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_view_overall_students_performance(tutor_base_url, selenium, teacher):
    """View the overall performance of students in scores page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at "student scores" page for with a finished assignment

    # WHEN: Click on the tab for the chosen period
    # AND: Click on the "Review" button under the selected reading or homework.

    # THEN: Each question has a correct response displayed


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_view_student_assignment_detail(tutor_base_url, selenium, teacher):
    """View student's assignment from score page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at "student scores" page with a finished assignment

    # WHEN: Click a student's score for a specific assignment

    # THEN: the teacher is taken to the assignment page with student's answers


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_no_score_is_displayed_for_readings(tutor_base_url, selenium, teacher):
    """Check no score for readings in the score page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at "student scores" page for a course with a finished reading

    # WHEN: Click on the "Student Scores" button
    # AND: Scroll to a reading assignment

    # THEN: The user is presented with progress icon but no score for reading


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_scores_info_icon(tutor_base_url, selenium, teacher):
    """Check the info icon in the score page displays proper information."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at "student scores" page for a course

    # WHEN: Click on the info icon next to "Class Performance"

    # THEN: The info icon displays a definition of how class and overall scores
    # are calculated.


@expected_failure
@test_case('')
@tutor
def test_accept_late_work(tutor_base_url, selenium, teacher):
    """Accept late work in the score page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Student has submitted late homework or readings for a course
    # AND: User is at "student scores" page for this course

    # WHEN: Scroll until an assignment with an orange triangle is found
    # AND: Click on the orange triangle at the upper right of a progress cell
    # AND: Click ""Accept late score"" OR "Accept late progress"

    # THEN: The late score replaces the score at due date


@expected_failure
@test_case('')
@tutor
def test_unaccept_late_work(tutor_base_url, selenium, teacher):
    """Unaccept late work in the score page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Teacher has admitted late homework or readings for a course
    # AND: User is at ""student scores"" page for this course

    # WHEN: Scroll until an assignment with an orange triangle is found
    # AND: Click on the orange triangle at the upper right of a progress cell
    # AND: Click "Use this score" OR "Use this Progress"

    # THEN: The score is converted back to the score at due date



@expected_failure
@nondestructive
@test_case('')
@tutor
def test_external_assignments_in_the_scores_export(tutor_base_url, selenium,
                                                   teacher):
    """Check that external assignments are not included in exported scores."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at "student scores" page for a course with an external

    # WHEN: Click "Export"

    # THEN: External assignments are not included in the scores export


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_dropped_students_in_student_scores(tutor_base_url, selenium, teacher):
    """Check removal of dropped students in scores page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at "student scores" page for a course with an dropped student

    # WHEN: Click on the period from which user have dropped the student

    # THEN: Dropped student should not be displayed in Student Scores


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_moved_students_in_student_scores(tutor_base_url, selenium, teacher):
    """Check moved students appear in their current sections in scores."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at "student scores" page for a course with an moved student

    # WHEN: Click on the period to which the student was moved

    # THEN: The user is presented with the moved student under their new period

@expected_failure
@nondestructive
@test_case('')
@tutor
def test_view_score_at_due_date(tutor_base_url, selenium, teacher):
    """Check teacher view scores at due date in score's page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course
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
    # AND: User is at "student scores" page for a course with an assignment

    # WHEN: Click on the orange flag in the upper right of a progress cell

    # THEN: The user is presented with current score"
