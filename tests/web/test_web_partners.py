"""Tests the tutor webpage."""

from tests.markers import nondestructive, skip_test, test_case, web


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_view_partners(web_base_url, selenium):
    """Tests the ability to view partners from the homepage."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Click "Technology"
    # AND: Click "openstax partners"
    # THEN: User is navigated to the OpenStax partners page
