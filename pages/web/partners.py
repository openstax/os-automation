"""OpenStax Partners."""

from selenium.webdriver.common.by import By

from pages.web.base import WebBase


class Partners(WebBase):
    """The OpenStax Partners page."""

    URL_TEMPLATE = '/partners'

    _banner_locator = (By.CLASS_NAME, 'partners-page')

    @property
    def loaded(self):
        """Return True if the hero banner is found."""
        return self.find_element(*self._banner_locator).is_displayed
