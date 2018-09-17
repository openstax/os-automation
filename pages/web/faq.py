"""The frequently asked questions page."""

from selenium.webdriver.common.by import By

from pages.web.base import WebBase


class FAQ(WebBase):
    """The OpenStax frequently asked questions."""

    URL_TEMPLATE = '/faq'

    _main_content_locator = (By.CLASS_NAME, 'page-loaded')

    @property
    def loaded(self):
        """Return True if the hero banner is found."""
        return self.find_element(*self._main_content_locator).is_displayed
