"""Test case for tutor page student interaction and activities."""

from tests.markers import expected_failure, nondestructive, test_case, tutor


@test_case('')
@expected_failure
@nondestructive
@tutor
def test_open_reading_assignment_page(tutor_base_url, selenium, student):
    """Test the tutor open reading assignment page."""
    # GIVEN: The Tutor home page logged as a student

    # AND: The student Has enrolled in a course

    # AND: The student has an open reading assignment in that course

    # WHEN: The user clicks on the reading assignment

    # THEN: The Reading page for a specific chapter loads


@test_case('')
@expected_failure
@nondestructive
@tutor
def test_reading_questions(tutor_base_url, selenium, student):
    """Test the reading questions."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a course

    # AND: Has an open reading assignment

    # WHEN: The user clicks on the reading assignment

    # AND: The user continues through the assignment

    # THEN: The review questions load

    # AND: The student is able to submit answers for all questions


@test_case('')
@expected_failure
@nondestructive
@tutor
def test_textbook_from_quiz(tutor_base_url, selenium, student):
    """Test the corresponding section of textbook from quiz."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a course

    # AND: Has an open reading assignment

    # WHEN: The user clicks on the reading assignment

    # AND: The user goes to an assessment

    # AND: The user clicks the "Comes from <section name>" link

    # THEN: The corresponding section of the textbook loads


@test_case('')
@expected_failure
@tutor
def test_dashboard_from_assignment_page(tutor_base_url, selenium, student):
    """Test the back to dashboard from reading assignment."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a course

    # AND: Has an open reading assignment

    # WHEN: The user finishes the reading

    # AND: The user clicks on the "Back to Dashboard" button

    # THEN: The student's dashboard for that course loads


@test_case('')
@expected_failure
@nondestructive
@tutor
def test_assignment_review_page(tutor_base_url, selenium, student):
    """Test the tutor assignment review."""
    # GIVEN: Logged into Tutor as a student

    # AND: Enrolled in a course

    # AND: Has a reading assignment

    # WHEN: The user clicks on the reading assignment

    # AND: The user clicks on the "Continue" button

    # THEN: The corresponding reading assignment review loads


@test_case('')
@expected_failure
@tutor
def test_spaced_practice_assessment(tutor_base_url, selenium, student):
    """Test the spaced practice assessment."""
    # GIVEN: Logged into Tutor as a student

    # AND: Enrolled in a course

    # AND: Has a reading assignment

    # AND: Has done at least three assignments before

    # WHEN: The user clicks on the reading assignment

    # AND: The user continues on the reading assignment

    # THEN: A Spaced Practice assessment is assigned


@test_case('')
@expected_failure
@tutor
def test_personalized_assessment(tutor_base_url, selenium, student):
    """Test the personalized assessment."""
    # GIVEN: Logged into Tutor as a student

    # AND: Enrolled in a course

    # AND: Has a reading assignment

    # WHEN: The user clicks on the reading assignment

    # AND: The user goes through readings and click "Continue" button

    # THEN: A Personalized assessment  is assigned


@test_case('')
@expected_failure
@tutor
def test_assignment_done_pop_up(tutor_base_url, selenium, student):
    """Test the pop up for  # WHEN assignment is finished."""
    # GIVEN: Logged into Tutor as a student

    # AND: Enrolled in a course

    # AND: Has a reading assignment

    # WHEN: The user click on the reading assignment

    # AND: The user completes the assignment

    # THEN: The user is shown "User are done"


@test_case('')
@expected_failure
@tutor
def test_complete_reading(tutor_base_url, selenium, student):
    """Test that complete reading assignment is shown on dashboard."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a course

    # AND: Has an open reading assignment

    # WHEN: The user selected the reading assignment

    # AND: The user works the assignment

    # AND: The user clicks "Back to Dashboard" button

    # THEN: The Dashboard page for that course loads

    # AND: The reading is marked "completed" on the dashboard
