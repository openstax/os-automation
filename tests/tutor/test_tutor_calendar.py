"""Test the Tutor teacher course calendar functions."""

from tests.markers import expected_failure, nondestructive, skip_test
from tests.markers import test_case, tutor


@test_case('C208664')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_view_the_instructor_calendar(tutor_base_url, selenium, teacher):
    """Test teacher to view the calendar."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN: Select a Tutor course

    # THEN: The teacher is presented their calendar dashboard


@test_case('C208665')
@skip_test(reason='Script not written')
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


@test_case('C208666')
@skip_test(reason='Script not written')
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


@test_case('C208667')
@skip_test(reason='Script not written')
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


@test_case('C208668')
@skip_test(reason='Script not written')
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


@test_case('C208669')
@skip_test(reason='Script not written')
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


@test_case('C208670')
@skip_test(reason='Script not written')
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


@test_case('C208671')
@skip_test(reason='Script not written')
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


@test_case('C208672')
@skip_test(reason='Script not written')
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


@test_case('C208673')
@expected_failure
@skip_test(reason='Webdriver cannot drag and drop Tutor assignments')
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


@test_case('C208674')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_add_assignment_to_past_day(tutor_base_url, selenium, teacher):
    """Test teacher to attempt to add and assignment to past day."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN: Select a Tutor course
    # AND: Click on a past day and drag assignments onto a past day""

    # THEN: User shouldn't be able to access past dates on calendar


@test_case('C208677')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_question_library_loads(tutor_base_url, selenium, teacher):
    """Test if question library works under teacher."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN:  Select a Tutor course
    # AND: Click question library from the calendar"

    # THEN: user should be taken to the question library


@test_case('C208694')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_nag_teachers_each_time_they_create_a_new_course(tutor_base_url,
                                                         selenium, teacher):
    """Fill in template."""


@test_case('C208695')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_nag_teachers_upon_their_second_login_or_session(tutor_base_url,
                                                         selenium, teacher):
    """Fill in template."""


@test_case('C208696')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_nag_reappears_if_user_select_i_dont_know_yet_option(tutor_base_url,
                                                             selenium,
                                                             teacher):
    """Fill in template."""


@test_case('C208699')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_nag_in_preview_course_every_2nd_assignment(tutor_base_url,
                                                    selenium, teacher):
    """Fill in template."""


@test_case('C208700')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_nag_in_preview_course_preview_expires(tutor_base_url,
                                               selenium, teacher):
    """Fill in template."""


@test_case('C208702')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_nag_in_preview_course_create_a_course_button(tutor_base_url,
                                                      selenium, teacher):
    """Fill in template."""


@test_case('C208703')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_setup_now_nag_appearing_on_first_initialization_of_preview_course(
        tutor_base_url, selenium, teacher):
    """Fill in template."""


@test_case('')
@skip_test(reason='Script not written, not matched to TestRail case')
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


@test_case('C208706')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_term_appearance_new(tutor_base_url, selenium, teacher):
    """Test terms/PP appearance for onboarding | new instructor."""
    # GIVEN:  Be at the Tutor page

    # WHEN: Log into verified teacher account
    # AND: Pick a course

    # THEN: In that course, the instructor is shown terms
    # AND:Once agreed, the instructor is taken to the course dashboard.


@test_case('C208707')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_term_appearance_exist(tutor_base_url, selenium, teacher):
    """Test terms/PP appearance for onboarding | existing instructor."""
    # GIVEN: Having changed the terms of a particular course as admin

    # WHEN: Log in as teacher and go to that course page.
    # AND: Enters a course.

    # THEN: the teacher is shown the terms when they changed.
    # AND: No changes should be made on the draft
