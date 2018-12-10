"""The press and marketing page."""

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

from pages.web.base import WebBase


class Press(WebBase):
    """The press and marketing page."""

    URL_TEMPLATE = '/press'

    _hero_quote_locator = (By.CSS_SELECTOR, '.hero h1')
    _press_releases_locator = (By.CSS_SELECTOR, '.press-releases')
    _sidebar_locator = (By.CSS_SELECTOR, '.sidebar')
    _news_mentions_locator = (By.CSS_SELECTOR, '.news-mentions')

    @property
    def loaded(self):
        """Return True when the four root elements are found."""
        selector = (
            By.CSS_SELECTOR,
            '{hero} , {press} , {sidebar} , {news}'
            .format(hero=self._hero_quote_locator[1],
                    press=self._press_releases_locator[1],
                    sidebar=self._sidebar_locator[1],
                    news=self._news_mentions_locator[1]))
        try:
            merged = self.find_elements(*selector)
            return len(merged) == 4
        except WebDriverException:
            return False

    def is_displayed(self):
        """Return True if the heading is displayed."""
        return self.find_element(*self._hero_quote_locator).is_displayed()
