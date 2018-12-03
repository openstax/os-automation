"""The OpenStax jobs board."""

from time import sleep

from selenium.webdriver.common.by import By

from pages.web.base import WebBase


class Careers(WebBase):
    """The OpenStax jobs board."""

    URL_TEMPLATE = '/careers'

    _banner_locator = (By.CSS_SELECTOR, '#main h1')
    _careers_content_locator = (By.CSS_SELECTOR, '[data-html=content]')

    @property
    def loaded(self):
        """Return True when text content is found."""
        return (
            len(self.find_element(*self._careers_content_locator)
                .text.strip()) > 0 and (sleep(1) or True))

    def is_displayed(self):
        """Return True if the heading is displayed."""
        return self.find_element(*self._banner_locator).is_displayed()
