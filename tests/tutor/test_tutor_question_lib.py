"""Test of teacher on question library."""

from tests.markers import expected_failure, nondestructive, test_case, tutor


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_back_to_performance_forecast(tutor_base_url, selenium, teacher):
    """Test teacher to go back to performance forecast."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN: Select a Tutor course
    # AND: Go to ""performance forecast""
    # AND: Go to dashboard/question library""

    # THEN: back to performance forecast"" button should be present
    # AND: clicking ""back to performance forecast"" button should
    # take user back to performance forecast page"


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_back_to_scores(tutor_base_url, selenium, teacher):
    """Test teacher to go back to scores."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course
    # AND: Select a Tutor course
    # AND: Go to student scores

    # WHEN:  Go to dashboard/performance forecast/question library""

    # THEN: back to scores"" button should be present
    # AND: clicking ""back to scores"" button should take user back to scores"


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_training_wheels(tutor_base_url, selenium, teacher):
    """Test teacher to use training wheels on question library page."""
    # GIVEN: A logged in teacher user

    # WHEN: Click on the ""Question Library"" button from the user dashboard
    # AND: Click on ""Help"" dropdown menu

    # AND: A super training wheel appears on the page
