"""Test case for tutor couse scores."""

from tests.markers import expected_failure, test_case, tutor


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
