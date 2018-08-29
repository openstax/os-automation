"""OpenStax Web's shared footer region."""

from time import sleep

from pypom import Region
from selenium.webdriver.common.by import By


class Footer(Region):
    """OpenStax Web footer region."""

    _root_locator = (By.ID, 'footer')
    _box_locator = (By.CLASS_NAME, 'hero-quote')
    _directory_locator = (By.CSS_SELECTOR, '[role=contentinfo]')
    _social_locator = (By.CLASS_NAME, 'social')

    @property
    def is_displayed(self):
        """Return true if the footer is currently displayed."""
        return self.is_displayed

    @property
    def box(self):
        """Access the box region."""
        region = self.find_element(*self._box_locator)
        return self.Box(self, region)

    @property
    def directory(self):
        """Access the directory."""
        region = self.find_element(*self._directory_locator)
        return self.Directory(self, region)

    @property
    def social(self):
        """Access the social services."""
        region = self.find_element(*self._social_locator)
        return self.SocialLinks(self, region)

    class Box(Region):
        """The footer's statement box."""

        @property
        def statement(self):
            """Return the hero banner statement."""
            return self.root.text

    class Directory(Region):
        """The site map directory links."""

        _license_locator = (By.CSS_SELECTOR, '[href$=license]')
        _terms_of_use_locator = (By.CSS_SELECTOR, '[href$=tos]')
        _privacy_policy_locator = (By.CSS_SELECTOR, '[href$=privacy-policy]')
        _accessibility_statement_locator = (By.CSS_SELECTOR,
                                            '[href*=accessibility]')
        _open_source_locator = (By.CSS_SELECTOR, '[href*=github]')
        _contact_us_locator = (By.CSS_SELECTOR, '[href$=contact]')
        _press_locator = (By.CSS_SELECTOR, '[href*=press]')
        _newsletter_locator = (By.LINK_TEXT, 'Newsletter')
        _nonprofit_statement_locator = (By.CSS_SELECTOR, 'p:first-child')
        _copyright_statement_locator = (By.CSS_SELECTOR, 'p:nth-child(2)')
        _ap_statement_locator = (By.TAG_NAME, 'ap-html')

        def view_licensing(self):
            """Go to the website license page."""
            self.find_element(*self._license_locator).click()
            sleep(1.0)
            from pages.web.license import License
            return License(self.driver)

        def view_the_terms_of_use(self):
            """View the terms of use."""
            self.find_element(*self._terms_of_use_locator).click()
            sleep(1.0)
            from pages.web.terms import Terms
            return Terms(self.driver)

        def view_the_privacy_policy(self):
            """View the privacy policy."""
            self.find_element(*self._privacy_policy_locator).click()
            sleep(1.0)
            from pages.web.privacy import PrivacyPolicy
            return PrivacyPolicy(self.driver)

        def view_the_accessibility_statement(self):
            """View the accessibility statement."""
            self.find_element(*self._accessibility_statement_locator).click()
            sleep(1.0)
            from pages.web.accessibility import Accessibility
            return Accessibility(self.driver)

        def view_the_code(self):
            """Open GitHub and view the OpenStax repositories."""
            self.find_element(*self._opens_source_locator).click()
            sleep(1.0)
            from pages.github.home import GitHub
            return GitHub(self.driver)

        def go_to_the_contact_form(self):
            """Go to the contact form."""
            self.find_element(*self._contact_us_locator).click()
            sleep(1.0)
            from pages.web.contact import Contact
            return Contact(self.driver)

        def view_press_releases(self):
            """View the press page."""
            self.find_element(*self._press_locator).click()
            sleep(1.0)
            from pages.web.press import Press
            return Press(self.driver)

        def go_to_the_newsletter_signup_form(self):
            """Go to the newsletter signup."""
            self.find_element(*self._newsletter_locator).click()
            sleep(1.0)
            from pages.web.newsletter import NewsletterSignup
            return NewsletterSignup(self.driver)

        @property
        def organization(self):
            """Return the OpenStax tax status statement."""
            return self.find_element(*self._nonprofit_statement_locator).text

        @property
        def copyright(self):
            """Return the OpenStax copyright statement."""
            return self.find_element(*self._copyright_statement_locator).text

        @property
        def ap_statement(self):
            """Return the AP statement."""
            return self.find_element(*self._ap_statement_locator).text

    class Social(Region):
        """OpenStax social program Links."""

        _facebook_locator = (By.CLASS_NAME, 'facebook')
        _twitter_locator = (By.CLASS_NAME, 'twitter')
        _linkedin_locator = (By.CLASS_NAME, 'linkedin')

        def go_to_facebook(self):
            """Go to OpenStax's Facebook page."""
            self.find_element(*self._facebook_locator).click()
            sleep(1.0)
            from pages.facebook.home import Facebook
            return Facebook(self.driver)

        def go_to_twitter(self):
            """Go to OpenStax's Twitter page."""
            self.find_element(*self._twitter_locator).click()
            sleep(1.0)
            from pages.twitter.home import Twitter
            return Twitter(self.driver)

        def go_to_linkedin(self):
            """Go to OpenStax's LinkedIn company page."""
            self.find_element(*self._linkedin_locator).click()
            sleep(1.0)
            from pages.linkedin.home import LinkedIn
            return LinkedIn(self.driver)
