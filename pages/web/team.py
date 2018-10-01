"""The OpenStax team and advisor page."""

from selenium.webdriver.common.by import By

from pages.web.base import WebBase


class Team(WebBase):
    """The OpenStax team and advisors page."""

    URL_TEMPLATE = '/team'

    _root_locator = (By.TAG_NAME, 'main')
    _hero_locator = (By.CSS_SELECTOR, '.hero h1')

    @property
    def loaded(self):
        """Return whether the hero banner is found."""
        return self.find_element(*self._hero_locator)

    def is_displayed(self):
        """Return True if the team page is displayed."""
        return self.find_element(*self._hero_locator).is_displayed()
