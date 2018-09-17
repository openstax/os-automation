"""OpenStax material adopters."""

from selenium.webdriver.common.by import By

from pages.web.base import WebBase


class Adopters(WebBase):
    """Adopters page."""

    URL_TEMPLATE = '/adopters'

    _loaded_locator = (By.CLASS_NAME, 'page-loaded')
    _institution_locator = (By.CSS_SELECTOR, 'main li')

    @property
    def loaded(self):
        """Wait until the institution list is displayed."""
        return (self.find_element(*self._loaded_locator).is_displayed
                and self.find_element(*self._institution_locator).is_displayed)

    @property
    def adopters(self):
        """Return the list of adopters."""
        return self.find_elements(*self._institution_locator)
