"""Tests for the OpenStax Web About Us page."""

from pages.web.about import AboutUs
from tests.markers import nondestructive, test_case, web


@test_case('C210378')
@nondestructive
@web
def test_the_about_us_panels_load(web_base_url, selenium):
    """Test for the presence of the About Us sections."""
    # GIVEN: a user viewing the about page
    about = AboutUs(selenium, web_base_url).open()

    # WHEN:

    # THEN: the "Who we are" section is displayed
    # AND:  the "What we do" section is displayed
    # AND:  the "Where we're going" section is displayed
    # AND:  the stats map is displayed
    assert(about.who_we_are.is_displayed)
    assert(about.what_we_do.is_displayed)
    assert(about.where_were_going.is_displayed)
    assert(about.content_map.is_displayed)


@test_case('C210379')
@nondestructive
@web
def test_who_we_are_links(web_base_url, selenium):
    """Test the links within the Who we are panel."""
    # GIVEN: a user viewing the about page
    about = AboutUs(selenium, web_base_url).open()

    # WHEN: they click on the "philanthropic foundations" link
    foundations = about.who_we_are.foundations()

    # THEN: the foundations page is displayed
    assert(foundations.loaded)

    # WHEN: they return to the about page
    # AND:  click on the "educational resource companies" link
    about.open()
    resources = about.who_we_are.resources()

    # THEN: the partners page is displayed
    assert(resources.loaded)

    # WHEN: they return to the about page
    # AND:  click on the "FAQ page" link
    about.open()
    faq = about.who_we_are.faq()

    # THEN: the faq page is displayed
    assert(faq.loaded)
