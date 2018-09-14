"""Tests for the OpenStax Web home page."""

from pages.web.home import WebHome as Home
from tests.markers import expected_failure, nondestructive, skip_test  # NOQA
from tests.markers import test_case, web  # NOQA


@test_case('C210296')
@nondestructive
@web
def test_the_website_loads(web_base_url, selenium):
    """Test if the OpenStax.org webpage loads."""
    # GIVEN: a web browser
    page = Home(selenium, web_base_url)

    # WHEN: a user opens the Web home page
    page.open()

    # THEN: the site loads
    assert(page.loaded), \
        '{page} did not load successfully'.format(page=web_base_url)
