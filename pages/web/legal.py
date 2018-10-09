"""The legal / intellectual property frequently asked questions page."""

from selenium.webdriver.common.by import By

from pages.web.base import WebBase


class License(WebBase):
    """The OpenStax.org licensing overview page."""

    URL_TEMPLATE = '/license'

    _root_locator = (By.CSS_SELECTOR, '#main')
    _heading_locator = (By.CSS_SELECTOR, 'h1')

    @property
    def loaded(self):
        """Return True when the heading is displayed."""
        return self.find_element(*self._heading_locator)

    def is_displayed(self):
        """Return True if the blog pinned article is displayed."""
        return self.loaded.is_displayed()
