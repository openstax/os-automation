"""The foundation and corporate supporters page."""

from selenium.webdriver.common.by import By

from pages.web.base import WebBase


class Supporters(WebBase):
    """The foundation and corporate supporters page."""

    URL_TEMPLATE = '/foundation'

    _root_locator = (By.TAG_NAME, 'main')
    _hero_locator = (By.CSS_SELECTOR, '.hero h1')

    @property
    def loaded(self):
        """Return whether the hero banner is found."""
        return self.find_element(*self._hero_locator)

    def is_displayed(self):
        """Return True if the supporters page is displayed."""
        return self.find_element(*self._hero_locator).is_displayed()
