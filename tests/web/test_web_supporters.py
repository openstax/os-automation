"""Test the foundation and corporate supporters page."""

from pages.web.home import WebHome
from tests.markers import nondestructive, test_case, web


@test_case('C210454')
@nondestructive
@web
def test_supporters_and_foundations_are_presented(web_base_url, selenium):
    """A list of companies and foundations supporting OpenStax is displayed."""
    # GIVEN: a user viewing the foundation page
    home = WebHome(selenium, web_base_url).open()
    supporters = home.openstax_nav.view_supporters()

    # WHEN:

    # THEN: the foundations are listed
    assert(supporters.is_displayed())
    assert('foundation' in supporters.location)
    assert(supporters.supporters), 'No organizations found'
