"""Test case for assignment interaction and activities."""

from tests.markers import expected_failure, test_case, tutor


@test_case('')
@expected_failure
@tutor
def test_homework_submit_button(tutor_base_url, selenium, student):
    """Test the homework submit button."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a course

    # AND: Is on a open homework assignment

    # WHEN: The user clicks one of the answer choices

    # THEN: The selected answer is light blue

    # AND: The submit button is orange


@test_case('')
@expected_failure
@tutor
def test_correct_answer(tutor_base_url, selenium, student):
    """Test the correct answer on the homework assignment."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a course

    # AND: Has an open homework assignment

    # WHEN: The user clicks an answer from the answer choice

    # AND: The user clicks the submit button

    # THEN: The correct answer is highlighted in red


@test_case('')
@expected_failure
@tutor
def test_assignment_error_page(tutor_base_url, selenium, student):
    """Test the tutor assignment error page."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a course

    # AND: Has an open homework assignment

    # WHEN: The user clicks the Report An Error button on the right
    # bottom corner

    # THEN: Taken to the error report page


@test_case('')
@expected_failure
@tutor
def test_assignment_from_link(tutor_base_url, selenium, student):
    """Test the tutor assignment comes from link."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a course

    # AND: Has an open homework assignment

    # WHEN: The user clicks on the "Comes from" link

    # THEN: Taken to specific textbook page corresponding to problem


@test_case('')
@expected_failure
@tutor
def test_dashboard_from_homework(tutor_base_url, selenium, student):
    """Test the back to dashboard button."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a course

    # AND: Has an open homework assignment

    # WHEN: The user finishes the homework

    # AND: The user clicks on the "Back to Dashboard" button

    # THEN: The Dashboard page for that course loads


@test_case('')
@expected_failure
@tutor
def test_previous_question(tutor_base_url, selenium, student):
    """Test the previous question icon."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a course

    # AND: Has an open homework assignment

    # AND: Has answered an assessment

    # WHEN: The user selects the homework assignment

    # AND: The user clicks on the previous question icon

    # THEN: The user is taken to the previous question


@test_case('')
@expected_failure
@tutor
def test_navigate_question(tutor_base_url, selenium, student):
    """Test the breadcrub of questions."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a course

    # AND: Has an open homework assignment

    # WHEN: The user clicks one of the section performance bars
    # from the dashboard

    # AND: The user clicks on a breadcrumb

    # THEN: Taken to the specific question that the user clicked on
