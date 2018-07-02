"""Tests the technology options webpage."""

from tests.markers import expected_failure, nondestructive, test_case, web


@test_case('')
@expected_failure
@nondestructive
@web
def test_view_technology_options(web_base_url, selenium):
    """Tests ability to view to technology options page."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Click "Technology"
    # AND: Click "Technology Options"
    # THEN: User can view the technology options page
