"""Test cases for performance forecast functionality."""

from tests.markers import expected_failure, nondestructive, skip_test  # noqa
from tests.markers import test_case, tutor  # noqa


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_user_performance_bar(tutor_base_url, selenium, student):
    """Test the user performance bar."""
    # GIVEN: Logged into Tutor as a student
    # AND: Has enrolled in a course

    # WHEN: The user clicks on the user performance bars of a enrolled course

    # THEN: The header bar, containing the course name, OpenStax logo,
    # and user menu link are visible.


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_performance_bar_question(tutor_base_url, selenium, student):
    """Test the performance bar questions."""
    # GIVEN: Logged into Tutor as a student
    # AND: Is on a course dashboard

    # WHEN: The user clicks on the section performance bar
    # AND: If there is a text box, input text

    # THEN: "Answer" button can be clicked


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_performance_bar_answer(tutor_base_url, selenium, student):
    """Test the performance bar answers."""
    # GIVEN: Logged into Tutor as a student
    # AND: Is on a course dashboard

    # WHEN: The user clicks one of the section performance bars
    # AND: If there is a text box, the user input text
    # AND: The user clicks the 'Answer' button

    # THEN: Text box disappears and the multiple choice answer appear


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_performance_bar_submit(tutor_base_url, selenium, student):
    """Test the performance bar submit button."""
    # GIVEN: Logged on Tutor as a student
    # AND: Is on a course dashboard

    # WHEN: The user clicks on one of the section of the performance bars
    # AND: The user filled out the text box and click on a multiple
    # choice answer

    # THEN: User should be able to click the submit button


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_performance_bar_assessment(tutor_base_url, selenium, student):
    """Test the performance bar assessment."""
    # GIVEN: Logged on Tutor as a student
    # AND: Has enrolled in a course

    # WHEN: The user clicks on one of the section of the performance
    # bars
    # AND: The user Filled out the text box and click on a multiple
    # choice answer
    # AND: The user clicks on submit button

    # THEN: The answer should be submited and user should be able to see
    # next question button


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_performance_bar_feedback(tutor_base_url, selenium, student):
    """Test the performance bar feedback."""
    # GIVEN: Logged on Tutor as a student
    # AND: Has enrolled in a course

    # WHEN: The user clicks on one of the section of the performance bars
    # AND: The user filled out the text box and click on a multiple choice
    # answer
    # AND: The user submit the answer

    # THEN: The correct answer and feedback should appear


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_performance_bar_breadcrumb(tutor_base_url, selenium, student):
    """Test the performance bar breadcrumb."""
    # GIVEN: Logged on Tutor as a student
    # AND: Has enrolled in a course

    # WHEN: The user clicks on one of the section of the performance bars
    # AND: The user filled out the text box and multiple choice
    # AND: The user submits the answer

    # THEN: Correctness for the completed question is visible in the breadcrumb


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_performance_forecast(tutor_base_url, selenium, student):
    """Test the performance forecast."""
    # GIVEN: Logged into Tutor as a student
    # AND: Is on a class dashboard

    # WHEN: The user clicks on the user menu in the upper right corner
    # AND: The user clicks on "Performance Forecast"

    # THEN:  Personal Performance Forecast is loaded


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_performance_forecast_info_icon_for_a_student(tutor_base_url, selenium,
                                                      student):
    """Test the performance forecast info icon."""
    # GIVEN: Logged into Tutor as a student
    # AND: Is on a class dahboard

    # WHEN: Click on "Performance Forecast"
    # AND: The user hovers the cursor over the info icon next to the header

    # THEN: Info icon shows an explanation of the data


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_performance_forecast_info_icon_for_a_teacher(tutor_base_url, selenium,
                                                      teacher):
    """View info icon in performance forecast page."""
    # GIVEN: Logged into Tutor as a teacher

    # AND: User is at a course's "performance forecast" page

    # WHEN: Hover the cursor over the info icon

    # THEN: Info icon shows an explanation of the data


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_performance_color_key(tutor_base_url, selenium, student):
    """Test the performance color key."""
    # GIVEN: Logged into Tutor as a student
    # AND: Is on a class dashboard

    # WHEN: The user clicks on the user menu in the upper right corner
    # of the page
    # AND: The user clicks on "Performance Forecast"

    # THEN: The performance color key is presented (next
    # to the 'Return to Dashboard' button)


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_performance_forecast_with_zero_question(
        tutor_base_url, selenium, student):
    """Test the performance forecast with zero questions."""
    # GIVEN: Logged into Tutor as a student
    # AND: Is on a class dashboard
    # AND: Has not done many questions before

    # WHEN: The user clicks on "Performance Forecast" on the user menu

    # THEN: Presented with blank performance forecast with no section
    # breakdowns and the words "User haven't worked enough problems
    # for Tutor to predict User's weakest topics."


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_performance_forecast_weak_area(tutor_base_url, selenium, student):
    """Test the weak area of the performance forecast."""
    # GIVEN: Logged into Tutor as a student
    # AND: Is on a class dashboard
    # AND: Has finished some assignments before

    # WHEN: The user clicks on "Performance Forecast" on the user menu

    # THEN: The user is presented with up to four problematic sections
    # under My Weaker Areas


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_performance_forecast_individual_section(
        tutor_base_url, selenium, student):
    """Test the individual sections of forecast."""
    # GIVEN: Logged into Tutor as a student
    # AND: Has enrolled in a class

    # WHEN: The user clicks on "Performance Forecast" on the user menu
    # AND: The user scrolls to Individual Chapters section

    # THEN: User is presented with chapters listed on top and their
    # sections below


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_performance_forecast_chapter(tutor_base_url, selenium, student):
    """Test the performance forecast chapter bar."""
    # GIVEN: Logged into Tutor as a student
    # AND: Has enrolled in a class

    # WHEN: The user clicks on "Performance Forecast" on the user menu
    # AND: The user scrolls to the Individual Chapters section
    # AND: The user clicks on a chapter bar

    # THEN: Page with up to five practice assessments for that
    # chapter is loaded


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_performance_forecast_section_bar(tutor_base_url, selenium, student):
    """Test the performance forecast section bar."""
    # GIVEN: Logged into Tutor as a student
    # AND: Has enrolled in a class

    # WHEN: The user clicks on "Performance Forecast" on the user menu
    # AND: The user scrolls to the Individual Chapters section
    # AND: The user clicks on a section bar

    # THEN: User is presented with up to five practice assessments for
    # that section


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_performance_forecast_without_data(tutor_base_url, selenium, student):
    """Test the performance forecast individual section without enough data."""
    # GIVEN: Logged into Tutor as a student
    # AND: Has enrolled in a class

    # WHEN: The user clicks on "Performance Forecast" on the user menu
    # AND: The user scrolls to the Individual Chapters section

    # THEN: User is presented with the "Practice More To Get Forecast"
    # button under a section without enough data instead of a color bar


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_performance_forecast_finished_assignment(
        tutor_base_url, selenium, student):
    """Test the performance forecast with finished assignment."""
    # GIVEN: Logged into Tutor as a student
    # AND: Has enrolled in a class
    # AND: Has finished an assignment

    # WHEN: Once an assignment is completed, the user clicks the
    # Performance Forecast

    # THEN: Performance forecast with the finished assignment updated is loaded


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_view_period_performance_forecast(tutor_base_url, selenium, teacher):
    """View performance forecast page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at a course's "performance forecast" page

    # WHEN: Click on the desired period

    # THEN: The period Performance Forecast is presented to the user


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_view_the_performance_color_key(tutor_base_url, selenium, teacher):
    """View performance color key in performance forecast page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click on "Performance Forecast" in the user menu

    # THEN: The performance color key is presented to the user


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_period_tabs_are_shown(tutor_base_url, selenium, teacher):
    """Check period tabs in performance forecast page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course
    # AND: Has more than one period

    # WHEN: Click on "Performance Forecast" in the user menu

    # THEN: The period tabs are shown to the user


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_period_with_zero_answers(tutor_base_url, selenium, teacher):
    """Check that a period with no answers doesn't show section breakdowns."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at the "performance forecast" page with no assignments

    # WHEN: Click on the period with zero answers

    # THEN: The user should see no section breakdowns


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_perforemance_forecast_weaker_areas(tutor_base_url, selenium, teacher):
    """Check weaker areas show up to four problematic sections."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at the "performance forecast" page with at least two period

    # WHEN: Click on the desired period

    # THEN: Weaker Areas show up to four problematic sections
