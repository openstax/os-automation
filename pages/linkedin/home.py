"""The OpenStax LinkedIn landing page."""

from pypom import Page
from selenium.webdriver.common.by import By


class LinkedIn(Page):
    """The OpenStax LinkedIn page."""

    URL_TEMPLATE = 'https://www.linkedin.com/company/openstax/'

    _header_nav_locator = (By.CSS_SELECTOR, '.nav')

    @property
    def loaded(self):
        """Return True if the authentication wall is found."""
        return 'authwall' in self.location

    def is_displayed(self):
        """Return True if the main content is loaded."""
        return self.find_element(*self._header_nav_locator).is_displayed()

    @property
    def location(self):
        """Return the current URL."""
        return self.driver.current_url
