"""Tests the tutor webpage."""

from tests.markers import nondestructive, skip_test, test_case, web


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_view_tutor(web_base_url, selenium):
    """Tests ability to view tutor from the homepage."""
    # GIVEN: On the OpenStax homepage.

    # WHEN: Click "Technology".
    # AND: Click "About OpenStax Tutor".
    # AND: Click "Get Started".

    # THEN: User is on accounts if not logged in, tutor if logged in.
