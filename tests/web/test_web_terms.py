"""Tests for the OpenStax Web terms of service and use."""

from pages.web.home import WebHome
from tests.markers import nondestructive, test_case, web


@test_case('C210376', 'C210377')
@nondestructive
@web
def test_the_terms_of_use_load(web_base_url, selenium):
    """The Terms of Use page loads."""
    # GIVEN: a web browser
    home = WebHome(selenium, web_base_url).open()

    # WHEN: a user opens the terms webpage
    terms = home.footer.directory.terms_of_use()

    # THEN: the page loads
    # AND:  there are multiple sections with text
    assert(terms.is_displayed())
    assert('/tos' in terms.location)
    assert(terms.title == 'Terms of Use')
    assert(terms.text)
