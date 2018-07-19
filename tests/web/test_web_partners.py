"""Tests the tutor webpage."""

from tests.markers import expected_failure, nondestructive, test_case, web


@test_case('')
@expected_failure
@nondestructive
@web
def test_view_partners(web_base_url, selenium):
    """Tests the ability to view partners from the homepage."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Click "Technology"
    # AND: Click "openstax partners"
    # THEN: User is navigated to the OpenStax partners page
