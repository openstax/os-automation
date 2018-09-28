"""The technology page."""

from selenium.webdriver.common.by import By

from pages.web.base import WebBase


class Technology(WebBase):
    """The technology options page."""

    URL_TEMPLATE = '/technology'

    _title_locator = (By.TAG_NAME, 'h1')

    @property
    def loaded(self):
        """Override the base loader."""
        return self.find_element(*self._title_locator)

    def is_displayed(self):
        """Return True if the technology page is displayed."""
        return self.find_element(*self._title_locator).is_displayed()
