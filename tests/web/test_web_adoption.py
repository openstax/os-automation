"""Test the adoption form."""

from pages.web.adoption import Adoption
from tests.markers import nondestructive, test_case, web


@test_case('C210385')
@nondestructive
@web
def test_adoption_form_loads(web_base_url, selenium):
    """Test the form loading."""
    # GIVEN: a user viewing the adoption page
    adoption = Adoption(selenium, web_base_url).open()

    # WHEN:

    # THEN: the form is displayed
    assert(adoption.loaded)


@test_case('C210386')
@nondestructive
@web
def test_adoption_form_links_to_the_interest_form(web_base_url, selenium):
    """Test the cross-form link."""
    # GIVEN: a user viewing the adoption page
    adoption = Adoption(selenium, web_base_url).open()

    # WHEN: they click on the "interest form" link
    interest = adoption.go_to_interest()

    # THEN: the interest page is displayed
    assert(interest.loaded)
