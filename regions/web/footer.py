"""Footer region"""

import time

from pypom import Region
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


class Footer(Region):
    """OpenStax navbar region."""

    _root_locator = (By.TAG_NAME, 'footer')

    _license_locator = (By.CSS_SELECTOR, "a[href*='license']")
    _terms_of_service_locator = (By.CSS_SELECTOR, "a[href*='tos']")
    _privacy_policy_locator = (By.CSS_SELECTOR, "a[href*='privacy-policy']")
    _accessibility_statement_locator = (By.CSS_SELECTOR, "a[href*='accessibility-statement']")
    _open_source_locator = (By.CSS_SELECTOR, "a[href*='https://github.com/openstax']")
    _contact_us_locator = (By.CSS_SELECTOR, "a[href*='contact']")
    _press_locator = (By.CSS_SELECTOR, "a[href*='press']")
    _newsletter_locator = (By.PARTIAL_LINK_TEXT, "Newsletter")
    _facebook_locator = (By.CLASS_NAME, 'facebook')
    _twitter_locator = (By.CLASS_NAME, 'twitter')
    _linkedin_locator = (By.CLASS_NAME, 'linkedin')

    @property
    def is_footer_displayed(self):
        """Footer display boolean."""
        return self.loaded

    def go_to_license(self):
        """Goes to the license page"""
        self.find_element(*self._license_locator).click()
        sleep(1)
        return License(self.driver)

    def go_to_tos(self):
        """Goes to the terms of service page"""
        self.find_element(*self._terms_of_service_locator).click()
        sleep(1)
        return TOS(self.driver)

    def go_to_privacy_policy(self):
        """Goes to the privacy policy page"""
        self.find_element(*self._privacy_policy_locator).click()
        sleep(1)
        return PrivacyPolicy(self.driver)

    def go_to_accessibility_statement(self):
        """Goes to the accessibility statement page"""
        self.find_element(*self._accessibility_statement_locator).click()
        sleep(1)
        return AccessibilityStatement(self.driver)

    def go_to_open_source(self):
        """Goes to the openstax github page"""
        self.find_element(*self._opens_source_locator).click()
        sleep(1)
        return GitHub(self.driver)

    def go_to_contact_us(self):
        """Goes to the contact page"""
        self.find_element(*self._contact_us_locator).click()
        sleep(1)
        return Contact(self.driver)

    def go_to_press(self):
        """Goes to the press page"""
        self.find_element(*self._press_locator).click()
        sleep(1)
        return Press(self.driver)

    def go_to_newsletter(self):
        """Goes to the newsletter page"""
        self.find_element(*self._newsletter_locator).click()
        sleep(1)
        return NewsletterSignup(self.driver)

    def go_to_facebook(self):
        """Goes to the facebook page"""
        self.find_element(*self._facebook_locator).click()
        sleep(1)
        return Facebook(self.driver)

    def go_to_twitter(self):
        """Goes to the twitter page"""
        self.find_element(*self._twitter_locator).click()
        sleep(1)
        return Twitter(self.driver)

    def go_to_linkedin(self):
        """Goes to the linkedin page"""
        self.find_element(*self._linkedin_locator).click()
        sleep(1)
        return Linkedin(self.driver)
