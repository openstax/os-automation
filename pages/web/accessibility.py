"""The OpenStax Web accessibility statement page."""

from selenium.webdriver.common.by import By

from pages.web.base import WebBase


class Accessibility(WebBase):
    """The accessibility statement."""

    URL_TEMPLATE = '/accessibility-statement'

    _section_locator = (By.CSS_SELECTOR, '#main h2')

    @property
    def loaded(self):
        """Wait until the statement is found."""
        return (super().loaded and self.find_element(*self._section_locator))

    def is_displayed(self):
        """Return True if the first statement header is displayed."""
        return self.loaded.is_displayed()

    @property
    def sections(self):
        """Access the section headers."""
        return self.find_elements(*self._section_locator)
