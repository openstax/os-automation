"""OpenStax Web's shared footer region."""

from pypom import Region
from selenium.webdriver.common.by import By

from utils.utilities import Utility, go_to_


class Footer(Region):
    """OpenStax Web footer region."""

    _root_locator = (By.ID, 'footer')
    _box_locator = (By.CLASS_NAME, 'hero-quote')
    _directory_locator = (By.CSS_SELECTOR, '[role=contentinfo]')
    _social_locator = (By.CLASS_NAME, 'social')

    @property
    def loaded(self):
        """Return True if the footer is currently displayed."""
        return self.root.is_displayed()

    def is_displayed(self):
        """Return True if the region is displayed."""
        return self.loaded

    @property
    def box(self):
        """Access the box region."""
        region_root = self.find_element(*self._box_locator)
        return self.Box(self, region_root)

    @property
    def directory(self):
        """Access the directory."""
        region_root = self.find_element(*self._directory_locator)
        return self.Directory(self, region_root)

    @property
    def social(self):
        """Access the social services."""
        region_root = self.find_element(*self._social_locator)
        return self.SocialLinks(self, region_root)

    def show(self):
        """Scroll the section into view."""
        Utility.scroll_to(self.driver, element=self.root)
        return self.page

    class Box(Region):
        """The footer's statement box."""

        @property
        def statement(self):
            """Return the hero banner statement."""
            return self.root.text.strip()

    class Directory(Region):
        """The site map directory links."""

        _license_locator = (By.CSS_SELECTOR, '[href$=license]')
        _terms_of_use_locator = (By.CSS_SELECTOR, '[href$=tos]')
        _privacy_policy_locator = (By.CSS_SELECTOR, '[href$=privacy-policy]')
        _accessibility_statement_locator = (By.CSS_SELECTOR,
                                            '[href*=accessibility]')
        _careers_locator = (By.CSS_SELECTOR, '[href$=careers]')
        _open_source_locator = (By.CSS_SELECTOR, '[href*=github]')
        _contact_us_locator = (By.CSS_SELECTOR, '[href$=contact]')
        _press_locator = (By.CSS_SELECTOR, '[href*=press]')
        _newsletter_locator = (By.LINK_TEXT, 'Newsletter')
        _nonprofit_statement_locator = (By.CSS_SELECTOR, 'p:first-of-type')
        _copyright_statement_locator = (By.CSS_SELECTOR, 'p:first-of-type ~ p')
        _ap_statement_locator = (By.TAG_NAME, 'ap-html')

        def view_licensing(self):
            """Go to the website license page."""
            Utility.safari_exception_click(
                self.driver, locator=self._license_locator)
            from pages.web.legal import License
            return go_to_(License(self.driver))

        def view_the_terms_of_use(self):
            """View the terms of use."""
            Utility.safari_exception_click(
                self.driver, locator=self._terms_of_use_locator)
            from pages.web.legal import Terms
            return go_to_(Terms(self.driver))

        def view_the_privacy_policy(self):
            """View the privacy policy."""
            Utility.safari_exception_click(
                self.driver, locator=self._privacy_policy_locator)
            from pages.web.legal import PrivacyPolicy
            return go_to_(PrivacyPolicy(self.driver))

        def view_the_accessibility_statement(self):
            """View the accessibility statement."""
            Utility.safari_exception_click(
                self.driver, locator=self._accessibility_statement_locator)
            from pages.web.accessibility import Accessibility
            return go_to_(Accessibility(self.driver))

        def view_openstax_career_opportunities(self):
            """View the careers page."""
            Utility.safari_exception_click(
                self.driver, locator=self._careers_locator)
            from pages.web.careers import Careers
            return go_to_(Careers(self.driver))

        def view_the_code(self):
            """Open GitHub and view the OpenStax repositories."""
            Utility.switch_to(
                self.driver, link_locator=self._open_source_locator)
            from pages.github.home import GitHub
            return go_to_(GitHub(self.driver))

        def go_to_the_contact_form(self):
            """Go to the contact form."""
            Utility.safari_exception_click(
                self.driver, locator=self._contact_us_locator)
            from pages.web.contact import Contact
            return go_to_(Contact(self.driver))

        def view_press_releases(self):
            """View the press page."""
            Utility.safari_exception_click(
                self.driver, locator=self._press_locator)
            from pages.web.press import Press
            return go_to_(Press(self.driver))

        def go_to_the_newsletter_signup_form(self):
            """Go to the newsletter signup."""
            Utility.safari_exception_click(
                self.driver, locator=self._newsletter_locator)
            from pages.web.newsletter import NewsletterSignup
            return go_to_(NewsletterSignup(self.driver))

        @property
        def organization(self):
            """Return the OpenStax tax status statement."""
            return self.find_element(*self._nonprofit_statement_locator).text

        @property
        def copyright(self):
            """Return the OpenStax copyright statement."""
            return (self.find_element(*self._copyright_statement_locator)
                    .text.replace('\n', ' ').strip())

        @property
        def ap_statement(self):
            """Return the AP statement."""
            return (self.find_element(*self._ap_statement_locator)
                    .text.replace('\n', ' ').strip())

    class SocialLinks(Region):
        """OpenStax social program Links."""

        _facebook_locator = (By.CLASS_NAME, 'facebook')
        _twitter_locator = (By.CLASS_NAME, 'twitter')
        _linkedin_locator = (By.CLASS_NAME, 'linkedin')
        _instagram_locator = (By.CLASS_NAME, 'instagram')

        def go_to_facebook(self):
            """Go to OpenStax's Facebook page."""
            facebook = self.find_element(*self._facebook_locator)
            url = facebook.get_attribute('href')[:-8]
            script = ('arguments[0].setAttribute("href", "{url}");'
                      .format(url=url))
            self.driver.execute_script(script, facebook)
            Utility.switch_to(
                self.driver, link_locator=self._facebook_locator)
            from pages.facebook.home import Facebook
            return go_to_(Facebook(self.driver))

        def go_to_twitter(self):
            """Go to OpenStax's Twitter page."""
            Utility.switch_to(
                self.driver, link_locator=self._twitter_locator)
            from pages.twitter.home import Twitter
            return go_to_(Twitter(self.driver))

        def go_to_linkedin(self):
            """Go to OpenStax's LinkedIn company page."""
            Utility.switch_to(
                self.driver, link_locator=self._linkedin_locator)
            from pages.linkedin.home import LinkedIn
            return go_to_(LinkedIn(self.driver))

        def go_to_instagram(self):
            """Go to OpenStax's Instagram page."""
            Utility.switch_to(
                self.driver, link_locator=self._instagram_locator)
            from pages.instagram.home import Instagram
            return go_to_(Instagram(self.driver))
