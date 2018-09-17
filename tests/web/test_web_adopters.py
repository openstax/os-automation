"""Test the adopters list."""

from pages.web.adopters import Adopters
from tests.markers import nondestructive, test_case, web


@test_case('C210384')
@nondestructive
@web
def test_adopting_institutions_are_listed(web_base_url, selenium):
    """Test for the presence of adopting institutions."""
    # GIVEN: a user viewing the adopters page
    adopters = Adopters(selenium, web_base_url).open()

    # WHEN:

    # THEN: a list of institutions is displayed
    assert(len(adopters.adopters) > 0), 'No institutions found'
