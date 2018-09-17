"""Test the OpenStax Web accessibility statement page."""

from pages.web.accessibility import Accessibility
from tests.markers import nondestructive, test_case, web
from utils.web import Web


@test_case('C210383')
@nondestructive
@web
def test_accessibility_statement_loads(web_base_url, selenium):
    """Test that the statement loads."""
    # GIVEN: a user viewing the accessibility statement page
    accessibility = Accessibility(selenium, web_base_url).open()

    # WHEN:

    # THEN: sections for "Web Accessibility", "Our progress", "Feedback",
    #       "Interactive Simulations", and "User-Contributed Content" are
    #       displayed
    for section in accessibility.sections:
        assert(section.text in Web.ACCESSIBILITY)
