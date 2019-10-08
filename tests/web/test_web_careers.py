"""Test the OpenStax jobs page."""

from pages.web.home import WebHome
from tests.markers import nondestructive, test_case, web
from utils.utilities import Utility


@test_case('C210408', 'C210409', 'C210410')
@nondestructive
@web
def test_open_positions_are_available(web_base_url, selenium):
    """Open positions are listed."""
    # GIVEN: a user viewing the careers page
    home = WebHome(selenium, web_base_url).open()
    careers = home.footer.directory.careers()

    # WHEN:

    # THEN: the position title is displayed
    # AND:  a link to the job post is available
    # AND:  the job posting on Rice Jobs is verified
    assert(careers.is_displayed()), 'Careers page not displayed'
    assert('careers' in careers.location), \
        f'"{selenium.current_url}" is not the Careers page'
    for position in careers.jobs:
        assert(position.title), 'Job title not found'
        assert(position.url), 'Job page URL not found'
        assert(Utility.test_url_and_warn(
            url=position.url,
            message=position.title,
            driver=selenium)), 'Rice Jobs page for the position in unavailable'
