"""Test the adoption form."""

from pages.web.adoption import Adoption
from tests.markers import nondestructive, test_case, web


@test_case('C210385')
@nondestructive
@web
def test_adoption_form_loads(web_base_url, selenium):
    """Test the for loading."""
    # GIVEN: a user viewing the adoption page
    adoption = Adoption(selenium, web_base_url).open()

    # WHEN:

    # THEN: the form is displayed
    assert(adoption.loaded)
