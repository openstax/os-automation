"""Test the impact page."""

from pages.web.home import WebHome
from tests.markers import nondestructive, test_case, web
from utils.utilities import Utility
from utils.web import Web


@test_case('C210437', 'C210438', 'C210439')
@nondestructive
@web
def test_the_our_impact_banner(web_base_url, selenium):
    """Test the features of the Our Impact banner region."""
    # GIVEN: a user viewing the impact page
    home = WebHome(selenium, web_base_url).open()
    impact = home.openstax_nav.view_our_impact()

    # WHEN:

    # THEN: "We measure our success in access." is displayed
    #       in the banner
    # AND:  "OpenStax has saved students" is displayed below
    #       the banner title
    assert(impact.is_displayed())
    assert('impact' in impact.location)
    assert('We measure our success in access.' in impact.banner)
    assert('OpenStax ha saved students' in impact.description)

    # WHEN: the window is reduced to 760 pixels wide
    impact.resize_window(width=Web.SMALL_TABLET)

    # THEN: "OpenStax has saved students" is not displayed
    #       below the banner title
    assert(not impact.subheading.is_displayed())


@test_case('C210440')
@nondestructive
@web
def test_organizations_are_directed_to_the_contact_form_for_more_information(
        web_base_url, selenium):
    """Organizations are directed to the contact form to receive more info."""
    # GIVEN: a user viewing the impact page
    home = WebHome(selenium, web_base_url).open()
    impact = home.openstax_nav.view_our_impact()

    # WHEN: the click on the "CONTACT US TO LEARN MORE" button
    contact = impact.contact_us()

    # THEN: the contact form is displayed
    # AND:  the subject is preset to "College/University Partnerships"
    assert(contact.is_displayed())
    assert('contact' in contact.location)
    assert('Partnerships' in contact.location)
    assert('Partnerships' in contact.topic)


@test_case('C210441')
@nondestructive
@web
def test_institutional_partner_logos_are_displayed(web_base_url, selenium):
    """Institutional Partner logos are presented."""
    # GIVEN: a user viewing the impact page
    home = WebHome(selenium, web_base_url).open()
    impact = home.openstax_nav.view_our_impact()

    # WHEN: they scroll below the banner
    impact.view_partners()

    # THEN: institutional partner logos are displayed
    for partner in impact.partners:
        assert(Utility.is_image_visible(selenium, image=partner.logo))


@test_case('C210442')
@nondestructive
@web
def test_users_may_view_adopting_institutions(web_base_url, selenium):
    """Users may view the list of institutions using OpenStax material."""
    # GIVEN: a user viewing the impact page
    home = WebHome(selenium, web_base_url).open()
    impact = home.openstax_nav.view_our_impact()

    # WHEN: they click on the "SEE A FULL LIST OF
    #       INSTITUTIONS THAT HAVE ADOPTED OPENSTAX" link
    adopters = impact.view_adopters()

    # THEN: the adopters page is displayed
    assert(adopters.is_displayed())
    assert('adopters' in adopters.location)
    assert(adopters.institutions)
