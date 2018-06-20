"""Test cases for performance forcast functionality."""

from tests.markers import expected_failure, test_case, tutor


@test_case('')
@expected_failure
@tutor
def test_user_performance_bar(tutor_base_url, selenium, student):
    """Test the user performance bar."""
    # GIVEN: Logged into Tutor as a studnet

    # AND: Has enrolled in a course

    # WHEN: The user clicks on a enrolled course

    # AND: The user clicks on the user performance bars

    # THEN: The header bar, containing the course name, OpenStax logo,
    # and user menu link are visible.


@test_case('')
@expected_failure
@tutor
def test_performance_bar_question(tutor_base_url, selenium, student):
    """Test the performance bar questions."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a course

    # WHEN: The user clicks on a enrolled course

    # AND: The user clicks one of the section performance
    # bars from the dashboard

    # AND: If there is a text box, input text

    # THEN: "Answer" button can be clicked


@test_case('')
@expected_failure
@tutor
def test_performance_bar_answer(tutor_base_url, selenium, student):
    """Test the performance bar answers."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a course

    # WHEN: The user clicks on a enrolled course

    # AND: The user clicks one of the section performance bars
    # from the dashboard

    # AND: If there is a text box, the user input text

    # AND: The user clicks the 'Answer' button

    # THEN: Text box disappears and the multiple choice answer appear


@test_case('')
@expected_failure
@tutor
def test_performance_bar_submit(tutor_base_url, selenium, student):
    """Test the performance bar submit button."""
    # GIVEN: Logged on Tutor as a student

    # AND: Has enrolled in a course

    # WHEN: The user clicks on one of the section of the performance bars

    # AND: The user filled out the text box and click on a multiple
    # choice answer

    # THEN: User should be able to click the submit button


@test_case('')
@expected_failure
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
@expected_failure
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
@expected_failure
@tutor
def test_performance_bar_breadcrumb(tutor_base_url, selenium, student):
    """Test the performance bar breadcrumb."""
    # GIVEN: Logged on Tutor as a student

    # AND: Has enrolled in a course

    # WHEN: The user clicks on one of the section of the performance bars

    # AND: The user filled out the text box

    # AND: The user clicks on a multiple choice answer

    # AND: The user submits the answer

    # THEN: Correctness for the completed question is visible in the breadcrumb


@test_case('')
@expected_failure
@tutor
def test_performance_forcast(tutor_base_url, selenium, student):
    """Test the performance forcast."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a class

    # WHEN: The user clicks on the user menu in the upper right corner

    # AND: The user clicks on "Performance Forecast"

    # THEN:  Personal Performance Forecast is loaded


@test_case('')
@expected_failure
@tutor
def test_performance_forcast_info_icon(tutor_base_url, selenium, student):
    """Test the performance forcast info icon."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a class

    # WHEN: The user goes into an enrolled class

    # AND: The user clicks on the user menu in the upper right
    # corner of the page

    # AND: The user clicks on "Performance Forecast"

    # AND: The user hovers the cursor over the info icon that is next to the
    # "Performance Forecast" header

    # THEN: Page with Info icon showing an explanation of the data is loaded


@test_case('')
@expected_failure
@tutor
def test_performance_color_key(tutor_base_url, selenium, student):
    """Test the performance color key."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a class

    # WHEN: The user goes into an enrolled class

    # AND: The user clicks on the user menu in the upper right corner
    # of the page

    # AND: The user clicks on "Performance Forecast"

    # THEN: The performance color key is presented (next
    # to the 'Return to Dashboard' button)


@test_case('')
@expected_failure
@tutor
def test_performance_forcast_with_zero_question(
        tutor_base_url, selenium, student):
    """Test the performance forcast with zero questions."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a class

    # AND: Has not done many questions before

    # WHEN: The user clicks on the user menu in the upper right corner

    # AND: The user clicks on "Performance Forecast"

    # THEN: Presented with blank performance forecast with no section
    # breakdowns and the words "User haven't worked enough problems
    # for Tutor to predict User's weakest topics."


@test_case('')
@expected_failure
@tutor
def test_performance_forcast_weak_area(tutor_base_url, selenium, student):
    """Test the weak area of the performance forcast."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a class

    # AND: Has finished some assignments before

    # WHEN: The user goes into an enrolled class

    # AND: The user clicks on the user menu in the upper right
    # corner of the page

    # AND: The user clicks on "Performance Forecast"

    # THEN: The user is presented with up to four problematic sections
    # under My Weaker Areas


@test_case('')
@expected_failure
@tutor
def test_performance_forcast_individual_section(
        tutor_base_url, selenium, student):
    """Test the individual sections of forcast."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a class

    # WHEN: The user clicks on the user menu in the upper right corner

    # AND: The user clicks on "Performance Forecast"

    # AND: The user scrolls to Individual Chapters section

    # THEN: User is presented with chapters listed on top and their
    # sections below


@test_case('')
@expected_failure
@tutor
def test_performance_forcast_chapter(tutor_base_url, selenium, student):
    """Test the performance forcast chapter bar."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a class

    # WHEN: The user goes to the enrolled class

    # AND: The user clicks on the user menu in the upper right corner

    # AND: The user clicks on "Performance Forecast"

    # AND: The user scrolls to the Individual Chapters section

    # AND: The user clicks on a chapter bar

    # THEN: Page with up to five practice assessments for that
    # chapter is loaded


@test_case('')
@expected_failure
@tutor
def test_performance_forcast_section_bar(tutor_base_url, selenium, student):
    """Test the performance forcast section bar."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a class

    # WHEN: The user clicks on the user menu in the upper right corner

    # AND: The user clicks on "Performance Forecast"

    # AND: The user scrolls to the Individual Chapters section

    # AND: The user clicks on a section bar

    # THEN: User is presented with up to five practice assessments for
    # that section


@test_case('')
@expected_failure
@tutor
def test_performance_forcast_without_data(tutor_base_url, selenium, student):
    """Test the performance forcast individual section without enough data."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a class

    # WHEN: The user clicks on the user menu in the upper right corner

    # AND: The user clicks on "Performance Forecast"

    # AND: The user scrolls to the Individual Chapters section

    # THEN: User is presented with the "Practice More To Get Forecast"
    # button under a section without enough data instead of a color bar


@test_case('')
@expected_failure
@tutor
def test_performance_forcast_finished_assignment(
        tutor_base_url, selenium, student):
    """Test the performance forcast with finished assignment."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a class

    # AND: Has finished an assignment

    # WHEN: Once an assignment is completed, the user clicks the
    # Performance Forecast

    # THEN: Performance forecast with the finished assignment updated is loaded
