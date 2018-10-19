"""OpenStax Partners."""

from selenium.webdriver.common.by import By

from pages.web.base import WebBase


class Partners(WebBase):
    """The OpenStax Partners page."""

    URL_TEMPLATE = '/partners'

    _banner_locator = (By.CSS_SELECTOR, '.container h1')

    @property
    def loaded(self):
        """Return True if the hero banner is found."""
        return 'OpenStax Partners' in self.driver.page_source

    def is_displayed(self):
        """Return True if the hero banner is displayed."""
        return self.find_element(*self._banner_locator).is_displayed()
