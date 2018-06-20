"""Tests the homepage."""

from tests.markers import expected_failure, nondestructive, test_case, web


@test_case('')
@expected_failure
@nondestructive
@web
def test_view_home(web_base_url, selenium):
    """Tests ability view homepage from other pages."""
    # GIVEN: On the OpenStax homepage.

    # WHEN: Click "About Us".
    # AND: Click the OpenStax logo on the upper left corner.

    # THEN: On homepage.
