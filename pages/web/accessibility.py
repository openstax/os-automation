"""The OpenStax Web accessibility statement page."""

from selenium.webdriver.common.by import By

from pages.web.base import WebBase


class Accessibility(WebBase):
    """The accessibility statement."""

    URL_TEMPLATE = '/accessibility-statement'

    _section_locator = (By.TAG_NAME, 'h2')

    @property
    def loaded(self):
        """Wait until the statement is displayed."""
        return self.find_element(*self._section_locator).is_displayed()

    @property
    def sections(self):
        """Access the section headers."""
        return self.find_elements(*self._section_locator)
