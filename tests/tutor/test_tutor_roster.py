"""Test case for tutor roster."""

from tests.markers import expected_failure, test_case, tutor


@test_case('')
@expected_failure
@tutor
def test_roster_period_page(tutor_base_url, selenium, teacher):
    """Test the roster period in preview course."""
    # GIVEN: Logged into Tutor as a teacher

    # AND: Has a preview course

    # WHEN: The user goes to the preview course

    # AND: Open the user menu

    # AND: Click on "Course Settings and Roster"

    # AND: Click on each period tabs shown

    # THEN:  Page with period with at least 3 students per section
    # is loaded
