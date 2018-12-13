"""OpenStax material adopters."""

from selenium.webdriver.common.by import By

from pages.web.base import WebBase


class Adopters(WebBase):
    """Adopters page."""

    URL_TEMPLATE = '/adopters'

    _institution_locator = (By.CSS_SELECTOR, 'main li')

    @property
    def loaded(self):
        """Wait until the institution list is displayed."""
        return len(self.adopters) > 0

    def is_displayed(self):
        """Return True if the adopters page is loaded."""
        return self.loaded

    @property
    def adopters(self):
        """Return the list of adopters."""
        return self.find_elements(*self._institution_locator)
