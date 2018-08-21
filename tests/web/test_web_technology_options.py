"""Tests the technology options webpage."""

from tests.markers import nondestructive, skip_test, test_case, web


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_view_technology_options(web_base_url, selenium):
    """Tests ability to view to technology options page."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Click "Technology"
    # AND: Click "Technology Options"
    # THEN: User can view the technology options page
