"""The Our Impact webpage."""

from selenium.webdriver.common.by import By

from pages.web.base import WebBase


class OurImpact(WebBase):
    """The Our Impact page."""

    URL_TEMPLATE = '/impact'

    _root_locator = (By.TAG_NAME, 'main')
    _hero_locator = (By.CSS_SELECTOR, '.hero h1')

    @property
    def loaded(self):
        """Return whether the hero banner text is found."""
        return self.find_element(*self._hero_locator)

    def is_displayed(self):
        """Return True if the hero statement is displayed."""
        return self.find_element(*self._hero_locator).is_displayed()
