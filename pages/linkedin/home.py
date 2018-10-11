"""The OpenStax LinkedIn landing page."""

from pypom import Page
from selenium.webdriver.common.by import By


class LinkedIn(Page):
    """The OpenStax LinkedIn page."""

    URL_TEMPLATE = 'https://www.linkedin.com/company/openstax/'

    _header_nav_locator = (By.CSS_SELECTOR, '.nav')

    @property
    def loaded(self):
        """Return True if the auth wall or company page is found."""
        return 'authwall' in self.location \
            or self.location == self.URL_TEMPLATE

    def is_displayed(self):
        """Return True if the main content is loaded."""
        return self.find_element(*self._header_nav_locator).is_displayed() \
            or self.loaded

    @property
    def location(self):
        """Return the current URL."""
        return self.driver.current_url
