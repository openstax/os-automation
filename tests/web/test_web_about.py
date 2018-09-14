"""Tests for the OpenStax Web About Us page."""

from pages.web.about import AboutUs
from tests.markers import nondestructive, test_case, web


@test_case('C210378')
@nondestructive
@web
def test_the_about_us_panels_load(web_base_url, selenium):
    """Test for the presence of the About Us sections."""
    # GIVEN: a user viewing the about page
    page = AboutUs(selenium, web_base_url).open()

    # WHEN:

    # THEN: the "Who we are" section is displayed
    # AND:  the "What we do" section is displayed
    # AND:  the "Where we're going" section is displayed
    # AND:  the stats map is displayed
    assert(page.who_we_are.is_displayed)
    assert(page.what_we_do.is_displayed)
    assert(page.where_were_going.is_displayed)
    assert(page.content_map.is_displayed)
