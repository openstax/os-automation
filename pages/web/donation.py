"""The gift and donation page."""

from selenium.webdriver.common.by import By

from pages.web.base import WebBase


class Give(WebBase):
    """The give page and form."""

    URL_TEMPLATE = '/give'

    _root_locator = (By.TAG_NAME, 'main')
    _banner_locator = (By.CSS_SELECTOR, '.hero h1')

    @property
    def loaded(self):
        """Return True when the banner heading is loaded."""
        return self.find_element(*self._banner_locator)

    def is_displayed(self):
        """Return True if the heading is displayed."""
        return self.find_element(*self._banner_locator).is_displayed()
