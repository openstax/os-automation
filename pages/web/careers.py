"""The OpenStax jobs board."""

from selenium.webdriver.common.by import By

from pages.web.base import WebBase


class Careers(WebBase):
    """The OpenStax jobs board."""

    URL_TEMPLATE = '/careers'

    _banner_locator = (By.CSS_SELECTOR, '#main h1')

    @property
    def loaded(self):
        """Return the banner element when the banner heading is found."""
        return self.find_element(*self._banner_locator)

    def is_displayed(self):
        """Return True if the heading is displayed."""
        return self.find_element(*self._banner_locator).is_displayed()
