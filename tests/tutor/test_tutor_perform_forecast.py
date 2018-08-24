"""Test of teacher functions."""

from tests.markers import nondestructive, skip_test, test_case, tutor


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_back_to_question_library(tutor_base_url, selenium, teacher):
    """Test teacher to go back to question library."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN: Go to question library
    # AND: Go to performance forecast/dashboard,
    # ""back to question library"" button should be present
    # AND: Click on the ""back to question library""

    # THEN: User is taken back to question library page


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_back_to_dashboard(tutor_base_url, selenium, teacher):
    """Test teacher to go back to dashboard."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN: go to performance forecast/question library,
    # ""back to dashboard"" button should be present
    # AND: Click on the ""Back to dashboard"" button""

    # THEN: User is taken back to the dashboard
