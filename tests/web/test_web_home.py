"""Tests for the OpenStax Web home page."""

from pages.web.home import WebHome as Home
from tests.markers import expected_failure, nondestructive, skip_test  # NOQA
from tests.markers import test_case, web  # NOQA


@test_case('')
@nondestructive
@web
def test_navigation_bars_are_present(web_base_url, selenium):
    """Test if the navigation bars are present."""
    page = Home(selenium, web_base_url)
    page.open()
