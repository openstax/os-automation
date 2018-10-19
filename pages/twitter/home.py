"""The OpenStax Twitter landing page."""

from pypom import Page
from selenium.webdriver.common.by import By


class Twitter(Page):
    """The OpenStax Twitter feed."""

    URL_TEMPLATE = 'https://twitter.com/openstax'

    _username_locator = (By.CSS_SELECTOR, '.ProfileHeaderCard-nameLink')

    @property
    def loaded(self):
        """Return True if the username is found."""
        return bool(self.find_element(*self._username_locator))

    def is_displayed(self):
        """Return True if the main content is loaded."""
        return self.find_element(*self._username_locator).is_displayed()

    @property
    def location(self):
        """Return the current URL."""
        return self.driver.current_url
