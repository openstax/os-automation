"""The OpenStax Covid-19 support page."""

from selenium.webdriver.common.by import By

from pages.web.base import WebBase


class OnlineResources(WebBase):
    """The Covid-19 support statement."""

    URL_TEMPLATE = '/general/online-resources'

    _section_locator = (
        By.CSS_SELECTOR, '#main .block-paragraph, #main .block-html')

    @property
    def loaded(self):
        """Wait until the statement is found."""
        return (super().loaded and self.find_element(*self._section_locator))

    def is_displayed(self):
        """Return True if the first statement header is displayed."""
        return self.find_element(*self._section_locator).is_displayed()

    @property
    def sections(self):
        """Access the section headers."""
        return self.find_elements(*self._section_locator)
