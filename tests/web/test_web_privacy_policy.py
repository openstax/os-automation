"""Test the OpenStax Web privacy policy page."""

from pages.web.home import WebHome
from tests.markers import nondestructive, test_case, web
from utils.utilities import Utility
from utils.web import Web


@test_case('C210448')
@nondestructive
@web
def test_the_privacy_policy_page(web_base_url, selenium):
    """Test the privacy policy page and GDPR access."""
    # GIVEN: a user viewing the privacy policy
    home = WebHome(selenium, web_base_url).open()
    Utility.scroll_bottom(selenium)
    privacy = home.footer.directory.view_the_privacy_policy()

    for section, heading in enumerate(privacy.sections):
        # WHEN: they scroll through the page
        privacy.view(section)

        # THEN: there are nine sections ("About this Privacy
        #       Policy", "Definitions", "Modifications",
        #       "Information We Collect", "How We Use Your
        #       Information", "Sharing Your Information",
        #       "Accuracy of Data, Storage", "Links to Other
        #       Websites", and "Security and Liability for
        #       Theft and/or Disclosure of Login
        #       Credentials")
        assert(heading in Web.PRIVACY)

    # WHEN: they click on the "gdpr.rice.edu" link
    gdpr = privacy.view_gdpr()

    # THEN: the Rice GDPR page is displayed in a new tab
    assert(gdpr.at_rice)
