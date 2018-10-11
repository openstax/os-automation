"""The OpenStax blog."""

from time import sleep

from selenium.webdriver.common.by import By

from pages.web.base import WebBase
from utils.utilities import Utility


class Blog(WebBase):
    """The OpenStax web log."""

    URL_TEMPLATE = '/blog'

    _root_locator = (By.TAG_NAME, 'main')
    _article_locator = (By.CSS_SELECTOR, '.articles .article:not(.hidden)')
    _initial_image_locators = (By.CSS_SELECTOR, '#main .img')
    _pinned_article_locator = (By.CLASS_NAME, 'pinned')

    @property
    def loaded(self):
        """Return True when all of the blog article images are loaded."""
        articles = self.find_elements(*self._article_locator)
        for article in articles:
            Utility.scroll_to(self.driver, element=article)
            sleep(0.25)
        Utility.scroll_top(self.driver)
        test = Utility.load_background_images(
            driver=self.driver,
            locator=self._initial_image_locators)
        sleep(3.0)
        return test

    def is_displayed(self):
        """Return True if the blog pinned article is displayed."""
        return self.find_element(*self._pinned_article_locator).is_displayed()
