"""Test of teacher on the calendar."""

from tests.markers import expected_failure, nondestructive, test_case, tutor


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_view_calendar(tutor_base_url, selenium, teacher):
    """Test teacher to view the calendar."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN: Select a Tutor course

    # THEN: The teacher is presented their calendar dashboard


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_view_student_score_w_calendar_button(tutor_base_url,
                                              selenium, teacher):
    """Test teacher to view student score with calendar button."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN: Select a Tutor course
    # AND: Click "Student Scores"

    # THEN: the teacher is presented with their students' scores
    # each section/period


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_view_performance_forecast_w_calendar_button(tutor_base_url,
                                                     selenium, teacher):
    """Test teacher to view performance forecast with calendar button."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN: Select a Tutor course
    # AND: Click "Performance Forecast"

    # THEN: the teacher is presented with performance forecast fot the sections


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_view_reading_assignment_summary(tutor_base_url, selenium, teacher):
    """Test teacher to view a reading assignment summary."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course
    # AND: has a reading assignment

    # WHEN: Select a Tutor course
    # AND: From the user calendar, click on a reading that is displayed

    # THEN: the teacher is presented with a summary of information about
    # the reading


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_view_homework_assignment_summary(tutor_base_url, selenium, teacher):
    """Test teacher to view a homework assignment ."""
    # GIVEN: A logged in teacher user
    # AND: has a homework assignment

    # WHEN: Select a Tutor course
    # AND: From the user calendar, click on a homework assignment
    # that is displayed"

    # THEN: The teacher is presented with a summary of the homework assignment.


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_view_external_assignment_summary(tutor_base_url, selenium, teacher):
    """Test teacher to view an external assignment."""
    # GIVEN: A logged in teacher user
    # AND: has an external assignment

    # WHEN: Select a Tutor course
    # AND: From the user calendar, click on external assignment
    # that is displayed""

    # THEN: The teacher is presented with a summary of the external
    # assignment.


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_view_event_summary(tutor_base_url, selenium, teacher):
    """Test teacher to view an event."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course
    # AND: has a event

    # WHEN:  Select a Tutor course
    # AND: From the user calendar, click on an event that is displayed""

    # THEN: The teacher is presented with a summary of the selected event.


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_open_reference_book_w_calendar_button(tutor_base_url,
                                               selenium, teacher):
    """Test teacher to open a reference book with calendar button."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN: Select a Tutor course
    # AND: Click on the 'Browse The Book' button on the user dashboard""

    # THEN: The teacher is presented with the book in a new tab


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_return_to_course_picker(tutor_base_url, selenium, teacher):
    """Test teacher return to course picker by clicking logo."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN: Select a Tutor course
    # AND: Click on the OpenStax logo at the top of the page""

    # THEN: The teacher should be returned to a page displaying
    # all of their courses.


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_add_by_drag(tutor_base_url, selenium, teacher):
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
@nondestructive
@test_case('')
@tutor
def test_add_assignment_to_past_day(tutor_base_url, selenium, teacher):
    """Test teacher to attempt to add and assignment to past day."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN: Select a Tutor course
    # AND: Click on a past day and drag assignments onto a past day""

    # THEN: User shouldn't be able to access past dates on calendar


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_question_library(tutor_base_url, selenium, teacher):
    """Test if question library works under teacher."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN:  Select a Tutor course
    # AND: Click ""question library"" from the calendar"

    # THEN: user should be taken to the question library


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_training_wheels_dashboard(tutor_base_url, selenium, teacher):
    """Test teacher to use training wheels for dashboard`."""
    # GIVEN: A logged in teacher user
    # AND: Click on a current course to navigate to Dashboard
    # AND: Activate Spy Mode
    # AND: Pop-up should show with the options
    # ""View Tips Now"" and ""View Later""

    # WHEN: Click ""View Tips Now""

    # THEN: User should be taken through a training wheels tour
    # detailing the creation of assignments,
    # the options at the top, the user dropdown options, and the navbar


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_term_appearance_new(tutor_base_url, selenium, teacher):
    """Test terms/PP appearance for onboarding | new instructor."""
    # GIVEN:  Be at the Tutor page

    # WHEN: Log into verified teacher account
    # AND: Pick a course

    # THEN: In that course, the instructor is shown terms
    # AND:Once agreed, the instructor is taken to the course dashboard.


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_term_appearance_exist(tutor_base_url, selenium, teacher):
    """Test terms/PP appearance for onboarding | existing instructor."""
    # GIVEN: Having changed the terms of a particular course as admin

    # WHEN: Log in as teacher and go to that course page.
    # AND: Enters a course.

    # THEN: the teacher is shown the terms when they changed.


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_physics_stu_preview_vidz(tutor_base_url, selenium, teacher):
    """Test teacher to embed physics student preview videos."""
    # GIVEN: A logged in teacher user

    # WHEN: Navigate to a Physics class
    # AND: Click on the small video icon on the top navbar

    # Dashboard preview: https://usertu.be/IbYU5py9YP8
    # Physics HW: https://usertu.be/Ic2_9LYXY84
    # Physics Reading: https://usertu.be/tCocd4jCVCA


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_soci_stu_preview_vidz(tutor_base_url, selenium, teacher):
    """Test teacher to embed sociology student preview videos."""
    # GIVEN: A logged in teacher user

    # WHEN:  Navigate to a Sociology class
    # AND: Click on the small video icon on the top navbar

    # THEN: User is taken to usertube videos with the following links:
    # Dashboard preview: https://usertu.be/IbYU5py9YP8
    # Soci HW: https://usertu.be/Ki-y2AywXlI
    # Soci Reading: https://usertu.be/GF05th84Bw8


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_bio_stu_preview_vidz(tutor_base_url, selenium, teacher):
    """Test teacher to embed biology student preview videos."""
    # GIVEN: A logged in teacher user

    # WHEN: Navigate to a Biology class
    # AND: Click on the small video icon on the top navbar

    # THEN: User is taken to usertube videos embedded with the following links:
    # Dashboard preview: https://usertu.be/IbYU5py9YP8
    # Bio HW: https://usertu.be/kzvHLFsQDTM
    # Bio Reading: https://usertu.be/4neNaHRyTUw
