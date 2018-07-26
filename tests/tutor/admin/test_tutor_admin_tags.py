"""Test of admin console tags page."""

from tests.markers import expected_failure, nondestructive, test_case, tutor


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_tag_searching(tutor_base_url, selenium, admin):
    """Test tag searching correctly searches."""
    # GIVEN: logged in as admin
    # AND: At the Tags page

    # WHEN: In the search bar enter a random word
    # AND: Click the ""Search"" button

    # THEN: Tags related to the entered word is correctly found and displayed
